using SumOfSquares
using DynamicPolynomials
using CSDP

@polyvar x y z a b c d
vars = [x,y,z,a,b,c,d]
q = (sum(r^2 for r in vars))^2
p = sum([sum([(abs((i-j)%7))<=1 ? 0 : vars[i]^2*vars[j]^2 for i=1:7]) for j=1:7])
f = 2*q-3*p
println(f)
solver = optimizer_with_attributes(CSDP.Optimizer)
model = SOSModel(solver)
t = 4
@constraint(model, f(x=>x^t, y=>y^t, z=>z^t, a=>a^t, b=>b^t, c=>c^t, d=>d^t) >= 0)
@objective(model, Max, 0)
JuMP.optimize!(model)

#
#
#@polyvar x y z w
#p=(400*w^4*x^2-800*w^3*x^3+400*w^2*x^4+486*w^4*x*y-1266*w^3*x^2*y+780*w^2*x^3*y+4431*w^4*y^2+1044*w^3*x*y^2+1266*w^2*x^2*y^2-8862*w^3*y^3-1530*w^2*x*y^3+4431*w^2*y^4+780*w^3*x^2*z-780*w^2*x^3*z-2752*w^3*x*y*z-2140*w^2*x^2*y*z+3954*w^2*x*y^2*z+600*w*x^2*y^2*z-2016*w^2*y^3*z-2002*w*x*y^3*z+2016*w*y^4*z+1180*w^2*x^2*z^2+100*x^4*z^2+600*w^2*x*y*z^2-820*w*x^2*y*z^2+2016*w^2*y^2*z^2+980*w*x*y^2*z^2+400*x^2*y^2*z^2-2016*w*y^3*z^2+400*y^4*z^2-200*x^3*z^3-780*w*x*y*z^3-800*y^3*z^3+100*x^2*z^4+400*y^2*z^4)
#solver = optimizer_with_attributes(CSDP.Optimizer)
#model = SOSModel(solver)
#@constraint(model, p >= 0)
#@objective(model, Max, 0)
#JuMP.optimize!(model)
#
##@polyvar x y z w
##
##p = x^2*y^2+x^2*z^2+x^2*w^2+y^2*z^2+y^2*w^2+z^2*w^2+  x^2*y*z+x^2*y*w+x^2*z*w+y^2*x*z+y^2*x*w+y^2*z*w+z^2*x*y+z^2*x*w+z^2*y*w+w^2*x*y+w^2*x*z+w^2*x*z   -4*x*y*z*w
##
##
##solver = optimizer_with_attributes(CSDP.Optimizer)
##model = SOSModel(solver)
##@constraint(model, (x^2+w^2)^2*p(x=>x, y=>x, z=>w, w=>w) >= 0)
##@objective(model, Max, 0)
##JuMP.optimize!(model)
#
#
##c = 0.001
##function optimize_sos(c1, c2)
##	solver = optimizer_with_attributes(CSDP.Optimizer, MOI.Silent()=>true)
##	model = SOSModel(solver)
##
##	@polyvar x y z
##
##	@variable(model, a)
##	@variable(model, b)
##
##	@constraint(model, (x^4+y^4+z^4)+c + a*(x^3+y^3+z^3) >= 0)
##	@objective(model, Max, c1*a + c2*b)
##	JuMP.optimize!(model)
##	return objective_value(model), value(a), value(b)
##end
##function optimize_nonneg(c1, c2)
##	solver = optimizer_with_attributes(CSDP.Optimizer, MOI.Silent()=>true)
##	model = SOSModel(solver)
##
##	@polyvar x y z
##
##	@variable(model, a)
##	@variable(model, b)
##
##	@constraint(model, (z^4+y^4+z^4)+c+a*(z^3+y^3+z^3) >= 0)
##	@objective(model, Max, c1*a + c2*b)
##	JuMP.optimize!(model)
##	return objective_value(model), value(a), value(b)
##end
#
##function main()
##	sos_pts = []
##	nonneg_pts = []
##	n = 100
##	for i=1:n
##		(o,x,y) = optimize_sos(cos(6.28*i/n), sin(6.28*i/n))
##		push!(sos_pts, (x,y))
##		(o,x,y) = optimize_nonneg(cos(6.28*i/n), sin(6.28*i/n))
##		push!(nonneg_pts, (x,y))
##		if i % 5 == 0
##			open("sos_pts.txt","a") do io
##			   for p in sos_pts
##				   x,y = p
##				   print(io,x)
##				   print(io,",")
##				   println(io,y)
##			   end 
##			end
##			open("nonneg_pts.txt","a") do io
##			   for p in nonneg_pts
##				   x,y = p
##				   print(io,x)
##				   print(io,",")
##				   println(io,y)
##			   end 
##			end
##			sos_pts = []
##			nonneg_pts = []
##		end
##	end
##end
###main()
##println(optimize_sos(-1,0))
##(o, a, b) = optimize_nonneg(-1,0)
##println(o)
##solver = optimizer_with_attributes(CSDP.Optimizer)
##model = SOSModel(solver)
#
##@polyvar x y z
##
##@constraint(model, (x^8+y^8+z^8)+0.01 + o*(x^6+y^6+z^6) >= 0)
##@objective(model, Max, 0)
##JuMP.optimize!(model)
