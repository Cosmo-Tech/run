import logging
import sys

from cosmotech_api import ApiClient, Configuration, MetaApi

from run.config import Config
from run.simulation import SimulationManager
from run.templates import BreweryTemplates

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Exit codes
EXIT_SUCCESS = 0
EXIT_ERROR = 1

def get_api_version(configuration):
    try:
        with ApiClient(configuration) as api_client:
            api_instance = MetaApi(api_client)
            api_response = api_instance.about()
            logger.info(api_response)
        return api_response.version
    except Exception as e:
        logger.error(f"Error retrieving API version: {str(e)}")
        raise e

def main() -> int:
    """Run the brewery simulation automation.

    Returns:
        Exit code indicating success (0) or failure (1)
    """
    try:
        # Load configuration from environment
        config = Config.from_env()
        logger.info("Starting brewery simulation automation")
        logger.info(f"Template directory: {config.template_dir}")
        # Load and validate templates
        templates = BreweryTemplates.load_from_directory(config.template_dir)
        templates.validate_templates()

        # Initialize API client
        configuration = Configuration(config.api_url)
        configuration.access_token = config.access_token

        get_api_version(configuration)

        with ApiClient(configuration) as api_client:
            # Initialize simulation manager
            sim_manager = SimulationManager(api_client=api_client)
            # Delete organization if already exists
            sim_manager.delete_organization(templates.organization["name"])
            organization = sim_manager.create_organization(templates.organization)
            # Create a solution within the organization
            solution = sim_manager.create_solution(
                org_id=organization.id, solution_template=templates.solution
            )
            templates.workspace["solution"]["solutionId"] = solution.id
            # Create a workspace within the organization using the solution ID
            workspace = sim_manager.create_workspace(
                org_id=organization.id, workspace_template=templates.workspace
            )
            templates.runner["solutionId"] = solution.id
            runner = sim_manager.create_runner(
                org_id=organization.id,
                workspace_id=workspace.id,
                runner_template=templates.runner,
            )
            run = sim_manager.start(organization.id, workspace.id, runner.id)
            status = sim_manager.wait_and_monitor_status(
                organization.id, workspace.id, runner.id, run.id
            )
            logs = sim_manager.get_run_logs(
                organization.id, workspace.id, runner.id, run.id
            )
            logger.info(f"organization id: {organization.id}")
            logger.info(f"solution id: {solution.id}")
            logger.info(f"workspace id: {workspace.id}")
            logger.info(f"runner id: {runner.id}")
            logger.info(f"status: {status.state.name}")
            logger.info("Run logs:")
            logger.info(logs)

            return EXIT_SUCCESS

    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        return EXIT_ERROR

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
