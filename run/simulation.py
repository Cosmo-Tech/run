# Simulation management for brewery automation script
import logging
from time import sleep, time

from cosmotech_api.api.organization_api import OrganizationApi
from cosmotech_api.api.run_api import RunApi
from cosmotech_api.api.runner_api import RunnerApi
from cosmotech_api.api.solution_api import SolutionApi
from cosmotech_api.api.workspace_api import WorkspaceApi
from cosmotech_api.models.organization_create_request import OrganizationCreateRequest
from cosmotech_api.models.runner_create_request import RunnerCreateRequest
from cosmotech_api.models.solution_create_request import SolutionCreateRequest
from cosmotech_api.models.workspace_create_request import WorkspaceCreateRequest

logger = logging.getLogger(__name__)


class SimulationManager:
    """Manages brewery simulation operations."""

    def __init__(self, api_client):
        self.organization_api = OrganizationApi(api_client)
        self.workspace_api = WorkspaceApi(api_client)
        self.solution_api = SolutionApi(api_client)
        self.runner_api = RunnerApi(api_client)
        self.run_api = RunApi(api_client)

    def start(self, organization_id, workspace_id, runner_id):
        run = self.runner_api.start_run(
            organization_id=organization_id,
            workspace_id=workspace_id,
            runner_id=runner_id,
        )
        logger.info(f"Started run {run}: {run.id}")
        return run

    def wait_and_monitor_status(self, organization_id, workspace_id, runner_id, run_id, max_time=120):
        """Monitor the execution of a run."""
        start_time = time()
        while True:
            try:
                status = self.run_api.get_run_status(
                    organization_id=organization_id,
                    workspace_id=workspace_id,
                    runner_id=runner_id,
                    run_id=run_id,
                )
                logger.info(f"Run status: {status.state.name}")
                if status.state.name in ["SUCCESSFUL", "FAILED"]:
                    return status
                if time() - start_time > max_time:
                    logger.error("Max monitoring time reached, exiting.")
                    return status
                sleep(1)
            except Exception as e:
                logger.error(f"Failed to monitor scenario: {str(e)}")
                raise

    def get_run_logs(self, organization_id, workspace_id, runner_id, run_id):
        """Fetch and log the output of a run."""
        try:
            logs = self.run_api.get_run_logs(
                organization_id=organization_id,
                workspace_id=workspace_id,
                runner_id=runner_id,
                run_id=run_id,
            )
            return logs
        except Exception as e:
            logger.error(f"Failed to fetch run logs: {str(e)}")
            raise

    def delete_organization(self, name):
        """Delete an organization."""
        organization_id = self.get_organization_id_by_name(name)
        if not organization_id:
            logger.info(f"Organization '{name}' does not exist. No deletion needed.")
            return
        # unregister organization
        try:
            self.organization_api.delete_organization(organization_id=organization_id)
            logger.info(f"Deleted organization: {organization_id}")
        except Exception as e:
            logger.error(f"Failed to delete organization: {str(e)}")
            raise

    def create_organization(self, organization_template):
        """Create a new organization.

        Args:
            organization_template (OrganizationCreateRequest): Template for organization creation.

        Returns:
            Organization: Organization object.
        """
        try:
            new_org = self.organization_api.create_organization(
                organization_create_request=OrganizationCreateRequest(
                    name=organization_template["name"],
                    security=organization_template["security"],
                )
            )
            logger.info(f"Created new organization: {new_org.name}: {new_org.id}")
        except Exception as e:
            logger.error(f"Failed to create organization: {str(e)}")
            raise
        return new_org

    def get_organization_id_by_name(self, organization_name):
        """Retrieve an organization's ID by its name."""
        try:
            organizations = self.list_organizations()
            for org in organizations:
                if org.name == organization_name:
                    logger.info(f"Found organization '{org.name}': {org.id}")
                    return org.id
            logger.warning(f"Organization '{organization_name}' not found")
            return None
        except Exception as e:
            logger.error(f"Failed to get organization ID: {str(e)}")
            raise

    def create_solution(self, org_id, solution_template):
        """Create a new solution."""
        try:
            new_solution = self.solution_api.create_solution(
                organization_id=org_id,
                solution_create_request=SolutionCreateRequest(
                    name=solution_template["name"],
                    key=solution_template["key"],
                    repository=solution_template["repository"],
                    version=solution_template["version"],
                    security=solution_template["security"],
                    runTemplates=solution_template["runTemplates"],
                ),
            )
            logger.info(f"Created new solution: {new_solution.name}: {new_solution.id}")
            return new_solution
        except Exception as e:
            logger.error(f"Failed to create solution: {str(e)}")
            raise

    def create_workspace(self, org_id, workspace_template):
        """Create a new workspace."""
        try:
            new_workspace = self.workspace_api.create_workspace(
                organization_id=org_id,
                workspace_create_request=WorkspaceCreateRequest(
                    name=workspace_template["name"],
                    key=workspace_template["key"],
                    solution=workspace_template["solution"],
                    security=workspace_template["security"],
                ),
            )
            logger.info(f"Created new workspace: {new_workspace.name}: {new_workspace.id}")
            return new_workspace
        except Exception as e:
            logger.error(f"Failed to create workspace: {str(e)}")
            raise

    def create_runner(self, org_id, workspace_id, runner_template):
        """Create a new runner."""
        try:
            new_runner = self.runner_api.create_runner(
                organization_id=org_id,
                workspace_id=workspace_id,
                runner_create_request=RunnerCreateRequest(
                    name=runner_template["name"],
                    solution_id=runner_template["solutionId"],
                    ownerName=runner_template["ownerName"],
                    run_template_id=runner_template["runTemplateId"],
                    security=runner_template["security"],
                ),
            )
            logger.info(f"Created new runner: {new_runner.name}: {new_runner.id}")
            return new_runner
        except Exception as e:
            logger.error(f"Failed to create runner: {str(e)}")
            raise

    # polyvalent functions while developing to be replaced by pure
    # create later
    def get_or_create_organization(self, organization_template):
        """Retrieve an organization or create one if it does not exist."""
        try:
            organizations = self.list_organizations()
            for org in organizations:
                if org.name == organization_template["name"]:
                    logger.info(f"Organization '{org.name}' already exists: {org.id}")
                    return org
            # Create organization if not found
            new_org = self.organization_api.create_organization(
                organization_create_request=OrganizationCreateRequest(
                    name=organization_template["name"],
                    security=organization_template["security"],
                )
            )
            logger.info(f"Created new organization: {new_org.name}")
            return new_org
        except Exception as e:
            logger.error(f"Failed to get or create organization: {str(e)}")
            raise

    def get_or_create_solution(self, org_id, solution_template):
        """Retrieve a solution or create one if it does not exist."""
        try:
            solutions = self.solution_api.list_solutions(
                organization_id=org_id, page=0, size=100
            )
            for sol in solutions:
                if sol.name == solution_template["name"]:
                    logger.info(f"Solution '{sol.name}' already exists: {sol.id}")
                    return sol
            new_solution = self.solution_api.create_solution(
                organization_id=org_id,
                solution_create_request=SolutionCreateRequest(
                    name=solution_template["name"],
                    key=solution_template["key"],
                    repository=solution_template["repository"],
                    version=solution_template["version"],
                    security=solution_template["security"],
                    runTemplates=solution_template["runTemplates"],
                ),
            )
            logger.info(f"Created new solution: {new_solution.name}")
            return new_solution
        except Exception as e:
            logger.error(f"Failed to get or create solution: {str(e)}")
            raise

    def get_or_create_workspace(self, org_id, workspace_template):
        """Retrieve a workspace or create one if it does not exist."""
        try:
            workspaces = self.workspace_api.list_workspaces(
                organization_id=org_id, page=0, size=100
            )
            for ws in workspaces:
                if ws.name == workspace_template["name"]:
                    logger.info(f"Workspace '{ws.name}' already exists: {ws.id}")
                    return ws

            # Create workspace if not found
            new_workspace = self.workspace_api.create_workspace(
                organization_id=org_id,
                workspace_create_request=WorkspaceCreateRequest(
                    name=workspace_template["name"],
                    key=workspace_template["key"],
                    solution=workspace_template["solution"],
                    security=workspace_template["security"],
                ),
            )
            logger.info(f"Created new workspace: {new_workspace.name}")
            return new_workspace
        except Exception as e:
            logger.error(f"Failed to get or create workspace: {str(e)}")
            raise

    def get_or_create_runner(self, org_id, workspace_id, runner_template):
        """Retrieve a runner or create one if it does not exist."""
        try:
            logger.info("trying to get runners")
            runners = self.runner_api.list_runners(
                organization_id=org_id, workspace_id=workspace_id
            )
            for runner in runners:
                if runner.name == runner_template["name"]:
                    logger.info(f"Runner '{runner.name}' already exists: {runner.id}")
                    return runner

            # Create runner if not found
            new_runner = self.runner_api.create_runner(
                organization_id=org_id,
                workspace_id=workspace_id,
                runner_create_request=RunnerCreateRequest(
                    name=runner_template["name"],
                    solution_id=runner_template["solutionId"],
                    ownerName=runner_template["ownerName"],
                    run_template_id=runner_template["runTemplateId"],
                    security=runner_template["security"],
                ),
            )
            logger.info(f"Created new runner: {new_runner.name}")
            return new_runner
        except Exception as e:
            logger.error(f"Failed to get or create runner: {str(e)}")
            raise

    def list_organizations(self):
        """Retrieve a list of organizations."""
        try:
            organizations = self.organization_api.list_organizations(page=0)
            logger.info(f"Retrieved {len(organizations)} organizations")
            return organizations
        except Exception as e:
            logger.error(f"Failed to retrieve organizations: {str(e)}")
            raise
