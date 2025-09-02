from jira import JIRA
from loguru import logger
from typing import List, Any

class JiraClient:
    """A client to interact with a Jira server."""

    def __init__(self, server: str, username: str, password: str):
        """
        Initializes the Jira client and connects to the server.

        Args:
            server: The URL of the Jira server.
            username: The username for authentication.
            password: The password for authentication.
        
        Raises:
            Exception: If the connection to Jira fails.
        """
        logger.debug(f"Connecting to Jira server: {server}")
        try:
            self.jira = JIRA(
                options = {
                    "server": server,
                    "verify": False  # Set to False to disable SSL verification (not recommended)
                },
                basic_auth=(username, password),
                
            )
        except Exception as e:
            logger.error(f"Failed to connect to Jira: {e}")
            raise  # Re-raise the exception to be handled by the caller

    def search_all_issues(self, jql: str) -> List[Any]:
        """
        Searches for all issues matching a JQL query, handling pagination.

        Args:
            jql: The JQL query string.

        Returns:
            A list of Jira issue objects.
        """
        logger.debug("Searching for issues...")
        logger.debug(f"JQL: {jql}")

        all_issues = []
        start_at = 0
        max_results = 100

        while True:
            logger.debug(f"Fetching issues from {start_at} to {start_at + max_results}")
            issues = self.jira.search_issues(jql, startAt=start_at, maxResults=max_results)
            if not issues:
                break
            all_issues.extend(issues)
            start_at += len(issues)

        logger.info(f"Found {len(all_issues)} issues.")
        return all_issues

    def iter_issues(self, jql: str, max_results: int = 100):
        """
        Iterator over Jira issues matching a JQL query, yielding one issue at a time.

        Args:
            jql: The JQL query string.
            max_results: Number of issues to fetch per request (pagination size).

        Yields:
            Jira issue objects, one by one.
        """
        logger.debug("Iterating issues...")
        logger.debug(f"JQL: {jql}")
        start_at = 0
        while True:
            logger.debug(f"Fetching issues from {start_at} to {start_at + max_results}")
            issues = self.jira.search_issues(jql, startAt=start_at, maxResults=max_results)
            if not issues:
                break
            for issue in issues:
                yield issue
            start_at += len(issues)
