using SumOfSquares
using DynamicPolynomials
using CSDP
import Polynomials

using Random

n = 5

@polyvar x[1:n]
e1 = (sum([x[i] for i in 1:n]))
e2 = sum([sum([x[i] * x[j] for i in (j+1):n]) for j in 1:(n-1)])
e3 = sum([sum([sum([x[i] * x[j] * x[k] for i in (k+1):n]) for k in (j+1):(n-1)]) for j in 1:(n-2)])
# Get a random stable cubic in n variables of the form
# a * ~e_3 + b ~e_2 ~e_1 + ~e_1^3
while true
	# Choose b randomly
	b = rand(Float64) + 1.33
	# Choose a so that -9*a*b^2-b^3+27*a^2 = 0
	sign = 2 * rand(0:1) - 1
	disc = b^3*(81*b-108)
	if disc < 0
		continue
	end
	a = (3*b^2-sign*sqrt(3*(4*b^3+3*b^4)))/18
	

	# Check that the other conditions are satisfied
	# 3/n^3 + b / ((n choose 2) n) >= 0
	if 3/(n^3) + b / ((n*(n-1))/2 * n) < 0
		continue
	end
	# 6/n^3 + 3*b/((n choose 2) n) + a >= 0
	if 6/(n^3) + 3 * b / ((n*(n-1))/2 * n) + a < 0
		continue
	end
	p = (a / (n*(n-1)*(n-2)/6) * e3 + b / ((n*(n-1))/2 * n) * e2 * e1 + e1^3 / n^3)
	for i in 1:10
		# Choose a random vector v, and then find a point on the boundary of the hyperbolicity cone in the v direction from (1,1,1,...)
		dirs = []
		for i in 1:2
			v = rand(Float64, n)
			v = v - [sum(v) / n for i in 1:n]	
			@polyvar t
			univar = p([x[i] => 1+t*v[i] for i in 1:n]...)
			coeffs = [coefficient(t) for t in terms(univar)]
			univar2 = Polynomials.Polynomial(reverse(coeffs))
			roots = (Polynomials.roots(univar2))
			if all([isreal(root) for root in roots])
				for root in roots
					if isreal(root) && root > 0
						push!(dirs, [1+root*v[n-i+1] for i in 1:n])
						break
					end
				end
			else
				for root in roots
					if isreal(root)
						push!(dirs, [1+root*v[n-i+1] for i in 1:n])
						break
					end
				end
			end
		end
		grad = [differentiate(p, x[i]) for i in 1:n]
		diffs = [sum([dir[i] * grad[i] for i in 1:n]) for dir in dirs]
		double_diff = sum([dirs[2][i] * differentiate(diffs[1],x[i]) for i in 1:n])
		wronsk = diffs[1] * diffs[2] - p * double_diff

		solver = optimizer_with_attributes(CSDP.Optimizer, MOI.Silent() => true)
		model = SOSModel(solver)
		@constraint(model, wronsk >= 0)
		@objective(model, Max, 0)
		JuMP.optimize!(model)
		if Int(primal_status(model)) != 1
			println("Not SOS!")
			println("a and b: ", a, " ", b)
			println("Polynomial: ", p)
			println("Directions: ", dirs)
			println("Wronskian: ", wronsk)
		end
	end
	
	break
end
