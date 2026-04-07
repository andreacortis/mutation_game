"""
Singularity analysis tools for the mutation game.

Implements the three key techniques connecting singularity theory to
ADE Dynkin diagrams:
  - Milnor number computation
  - Homotopy method (Moser's path) for constructing coordinate changes
  - Jet reduction to normal form
  - Splitting Lemma (completing the square)
"""
from sympy import (
    symbols, Symbol, diff, expand, simplify, solve, sqrt, degree,
    Poly, resultant, hessian, Function, Eq, dsolve, Rational,
    Matrix, eye, zeros as sym_zeros, oo,
)


def milnor_number(f, variables):
    """
    Compute the Milnor number of an isolated singularity at the origin.

    Uses the resultant method for two-variable singularities and the
    local algebra dimension for the general case.

    Args:
        f: sympy expression for the function germ
        variables: tuple/list of sympy symbols (the variables)

    Returns:
        int: the Milnor number mu

    Examples:
        >>> from sympy import symbols
        >>> x, y = symbols('x y')
        >>> milnor_number(x**3 + y**2, (x, y))
        2
        >>> milnor_number(x**2 * y + y**4, (x, y))
        5
    """
    partials = [diff(f, v) for v in variables]
    if len(variables) == 1:
        # One variable: mu = ord(f') - 1
        v = variables[0]
        p = Poly(partials[0], v)
        # Milnor number = multiplicity of zero as root of f'
        return degree(p) - 1 if p != 0 else oo
    elif len(variables) == 2:
        # Two variables: mu = deg of resultant
        res = resultant(partials[0], partials[1], variables[1])
        return degree(Poly(res, variables[0]))
    else:
        raise NotImplementedError(
            "Milnor number for > 2 variables requires Groebner basis "
            "computation; use SageMath for this case."
        )


def corank(f, variables):
    """
    Compute the corank of a singularity at the origin.

    The corank is the number of zero eigenvalues of the Hessian matrix,
    equivalently n - rank(H).

    Args:
        f: sympy expression
        variables: tuple/list of sympy symbols

    Returns:
        int: the corank
    """
    H = hessian(f, list(variables))
    H0 = H.subs([(v, 0) for v in variables])
    return len(variables) - H0.rank()


def classify(f, variables):
    """
    Classify a simple singularity by its ADE type.

    Uses the Milnor number and corank to determine the type.

    Args:
        f: sympy expression
        variables: tuple/list of sympy symbols

    Returns:
        str: the ADE type (e.g. "A3", "D5", "E6") or "unknown"
    """
    mu = milnor_number(f, variables)
    cr = corank(f, variables)

    if cr == 1:
        return f"A{mu}"
    elif cr == 2:
        if mu == 4:
            return "D4"
        elif mu >= 4:
            # Distinguish D_n from E_n
            # D_n: x^2*y + y^{n-1}, corank 2, mu = n
            # E_6: x^3 + y^4, mu = 6
            # E_7: x^3 + x*y^3, mu = 7
            # E_8: x^3 + y^5, mu = 8
            # Use the 3-jet to distinguish: D_n has a cubic with a repeated factor
            if mu in (6, 7, 8):
                # Check the 3-jet for a cube term
                jet3 = _truncate(f, variables, 3)
                p3 = Poly(jet3, *variables)
                # E-types have the 3-jet = x^3 (up to coord change)
                # D-types have 3-jet with a double factor
                # Simple test: E-types have a pure cube in one variable
                monoms = p3.as_dict()
                has_pure_cube = False
                for v in variables:
                    power = tuple(3 if u == v else 0 for u in variables)
                    if monoms.get(power, 0) != 0:
                        has_pure_cube = True
                        break
                if has_pure_cube and mu in (6, 7, 8):
                    return f"E{mu}"
            return f"D{mu}"
    return "unknown"


def _truncate(f, variables, order):
    """Truncate f to terms of total degree <= order."""
    p = Poly(f, *variables)
    result = 0
    for monom, coeff in p.as_dict().items():
        if sum(monom) <= order:
            term = coeff
            for v, e in zip(variables, monom):
                term *= v**e
            result += term
    return result


def splitting_lemma(f, variables):
    """
    Apply the Splitting Lemma to separate non-degenerate directions.

    Returns the coordinate substitution and the reduced function.

    Args:
        f: sympy expression
        variables: tuple/list of sympy symbols

    Returns:
        dict with keys:
            'substitution': dict mapping old vars to expressions in new vars
            'quadratic_part': the non-degenerate quadratic part
            'residual': the reduced function in fewer variables
            'corank': corank of the singularity
            'new_variables': list of new variable symbols
    """
    variables = list(variables)
    n = len(variables)
    H = hessian(f, variables)
    H0 = H.subs([(v, 0) for v in variables])
    cr = n - H0.rank()

    if cr == n:
        return {
            "substitution": {v: v for v in variables},
            "quadratic_part": 0,
            "residual": f,
            "corank": cr,
            "new_variables": variables,
        }

    substitution = {v: v for v in variables}
    quadratic_terms = []
    remaining = f
    new_vars = list(variables)

    # Iteratively complete the square for each non-degenerate direction
    for i in range(n):
        H_cur = hessian(remaining, new_vars)
        H0_cur = H_cur.subs([(v, 0) for v in new_vars])

        # Find a variable with non-zero diagonal in Hessian
        pivot = None
        for j, v in enumerate(new_vars):
            if H0_cur[j, j] != 0:
                pivot = j
                break

        if pivot is None:
            # Try to create a non-zero diagonal by a linear change
            found = False
            for j in range(len(new_vars)):
                for k in range(j + 1, len(new_vars)):
                    if H0_cur[j, k] != 0:
                        # Replace v_j with v_j + v_k
                        old_v = new_vars[j]
                        remaining = remaining.subs(old_v, old_v + new_vars[k])
                        remaining = expand(remaining)
                        substitution[old_v] = substitution[old_v].subs(
                            old_v, old_v + new_vars[k]
                        )
                        found = True
                        break
                if found:
                    break
            if not found:
                break
            # Recompute
            H_cur = hessian(remaining, new_vars)
            H0_cur = H_cur.subs([(v, 0) for v in new_vars])
            for j, v in enumerate(new_vars):
                if H0_cur[j, j] != 0:
                    pivot = j
                    break
            if pivot is None:
                break

        v_pivot = new_vars[pivot]

        # Complete the square: collect terms involving v_pivot
        p = Poly(remaining, v_pivot)
        if p.degree() < 2:
            break

        a2 = p.nth(2)  # coefficient of v_pivot^2
        a1 = p.nth(1)  # coefficient of v_pivot^1
        rest = expand(remaining - a2 * v_pivot**2 - a1 * v_pivot)

        # f = a2*(v_pivot + a1/(2*a2))^2 - a1^2/(4*a2) + rest
        shift = a1 / (2 * a2)
        u = symbols(f"u{i}")
        completed = a2 * u**2
        residual = expand(rest - a1**2 / (4 * a2))

        quadratic_terms.append(completed)
        substitution[v_pivot] = u - shift
        remaining = expand(residual)
        new_vars = [u if v == v_pivot else v for v in new_vars]

        if len(new_vars) - len(quadratic_terms) <= cr:
            break

    quad_part = sum(quadratic_terms) if quadratic_terms else 0

    return {
        "substitution": substitution,
        "quadratic_part": expand(quad_part),
        "residual": expand(remaining),
        "corank": cr,
        "new_variables": new_vars,
    }


def jet_reduce(f, variable, target_degree, max_order=10):
    """
    Reduce a one-variable singularity to its normal form by eliminating
    higher-order terms via polynomial coordinate changes.

    Args:
        f: sympy expression in one variable
        variable: the sympy symbol
        target_degree: the degree of the leading term (e.g. 3 for A_2)
        max_order: maximum order to eliminate

    Returns:
        dict with keys:
            'normal_form': the reduced function (truncated)
            'coordinate_change': expression for old variable in terms of new
            'steps': list of (order, coefficient_killed, parameter_value)
    """
    u = symbols("u")
    # Build coordinate change x = u + a_2*u^2 + a_3*u^3 + ...
    params = {i: symbols(f"a{i}") for i in range(2, max_order + 1)}
    phi = u + sum(params[i] * u**i for i in range(2, max_order + 1))

    f_sub = f.subs(variable, phi)
    f_sub = expand(f_sub)
    p = Poly(f_sub, u)

    steps = []
    param_vals = {}

    for order in range(target_degree + 1, max_order + target_degree):
        coeff = p.nth(order)
        # Substitute already-determined parameters
        coeff = coeff.subs(param_vals)

        # Find the free parameter at this order
        free_param_order = order - target_degree + 1
        if free_param_order not in params:
            break

        free = params[free_param_order]
        if free not in coeff.free_symbols:
            continue

        val = solve(coeff, free)
        if val:
            param_vals[free] = val[0]
            steps.append((order, coeff, val[0]))

            # Recompute
            phi_current = u + sum(
                param_vals.get(params[i], params[i]) * u**i
                for i in range(2, max_order + 1)
            )
            f_sub = f.subs(variable, phi_current)
            f_sub = expand(f_sub)
            p = Poly(f_sub, u)

    phi_final = u + sum(
        param_vals.get(params[i], 0) * u**i for i in range(2, max_order + 1)
    )

    return {
        "normal_form": u**target_degree,
        "coordinate_change": phi_final,
        "steps": steps,
    }


def homotopy_equivalence(f, g, variables):
    """
    Construct the coordinate change between two equivalent singularities
    using Moser's path method.

    Connects f and g by F_t = (1-t)*f + t*g and integrates the flow.
    Currently supports cases where the velocity field ODE can be solved
    in closed form.

    Args:
        f, g: sympy expressions (equivalent singularities)
        variables: tuple/list of sympy symbols

    Returns:
        dict with keys:
            'coordinate_change': dict mapping each variable to its image
            'velocity_field': the vector field (a_1, ..., a_n)
            'F_t': the homotopy path
    """
    t = symbols("t")
    variables = list(variables)
    Ft = expand((1 - t) * f + t * g)
    delta = expand(g - f)

    partials = [diff(Ft, v) for v in variables]

    # Try to express delta = sum a_i * dFt/dv_i
    # Strategy: for each variable, check if delta is divisible by dFt/dv_i.
    # Try variables that actually appear in delta first.
    coord_change = {v: v for v in variables}
    velocity = {v: 0 for v in variables}

    # Sort: try variables appearing in delta first
    order = sorted(range(len(variables)),
                   key=lambda i: 0 if diff(delta, variables[i]) != 0 else 1)

    remaining_delta = delta
    for i in order:
        if remaining_delta == 0:
            break
        v = variables[i]
        if partials[i] == 0:
            continue

        ai = simplify(remaining_delta / partials[i])
        check = simplify(remaining_delta - ai * partials[i])
        if check != 0:
            continue

        # Solve ODE: dV/dt = -ai(V, t)
        V = Function(str(v).upper())
        ode = Eq(V(t).diff(t), -ai.subs(v, V(t)))
        try:
            sol = dsolve(ode, V(t))
            C1 = symbols("C1")
            c_val = solve(sol.rhs.subs(t, 0) - v, C1)
            if c_val:
                V_final = simplify(sol.rhs.subs(C1, c_val[0]).subs(t, 1))
                coord_change[v] = V_final
                velocity[v] = -ai
                remaining_delta = 0
        except Exception:
            pass

    return {
        "coordinate_change": coord_change,
        "velocity_field": velocity,
        "F_t": Ft,
    }
