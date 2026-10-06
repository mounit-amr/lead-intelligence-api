from src.schemas import ICP


def validate_icp(icp: ICP) -> ICP:
    if not any([
        icp.industries,
        icp.countries,
        icp.employees_min is not None,
        icp.employees_max is not None,
        icp.revenue_min is not None,
        icp.funding_min is not None,
        icp.budget_min is not None
    ]):
        raise ValueError("ICP must contain at least one criterion")

    return icp