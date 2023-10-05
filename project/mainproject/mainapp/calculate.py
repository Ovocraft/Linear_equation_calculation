from pulp import LpProblem, LpVariable, LpMaximize
from pulp import LpStatus

def solve_equations(date_yueshu, date_xishu, date_zuizhi_value, belong_user_row):
    model = LpProblem(name="User_Equation_Problem", sense=LpMaximize)

    # 动态创建变量
    variables = [LpVariable(name=f"x{i+1}", lowBound=0) for i in range(0, belong_user_row)]

    # 添加约束条件
    for eq in date_yueshu:
        coeffs = [c.value for c in eq.coefficients.all()]  
        constraint_value = eq.constraint_value  
        sign = eq.sign  

        lp_exp = sum(c * v for c, v in zip(coeffs, variables))

        if sign == "<":
            model += lp_exp <= constraint_value, eq.id
        elif sign == ">":
            model += lp_exp >= constraint_value, eq.id
        elif sign == "=":
            model += lp_exp == constraint_value, eq.id

    # 添加目标函数
    objective_exp = sum(c * v for c, v in zip(date_zuizhi_value, variables))
    model += objective_exp, "Objective"

    # 求解模型
    model.solve()

    # 获取解决方案
    solution = {f"x{i+1}": variables[i].varValue for i in range(0, belong_user_row)}

    if model.status == 1:
        status = "Feasible"
        solution = {f"x{i+1}": variables[i].varValue for i in range(0, belong_user_row)}
    else:
        status = "Infeasible"
        solution = None

    result = {
        "status": status, 
        "num_vars": model.numVariables,
        "num_constraints": model.numConstraints,
        "var_names": [v.name for v in variables],
        "constraints": model.constraints,
        "solution": solution,
            }
    return result
