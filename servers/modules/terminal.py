import asyncio
from typing import Dict, Any, Optional
import argparse
import logging
from mcp.server.fastmcp import FastMCP
from . import MCPModule

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TerminalModule:
    def __init__(self):
        self._mcp = FastMCP("terminal")
        self._mcp_server = self._mcp._mcp_server
        self._current_process = None
        self._current_working_directory = None

    def register_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Register command line arguments for the terminal module."""
        parser.add_argument(
            '--working-directory',
            help='Default working directory for terminal commands'
        )

    def initialize(self, args: argparse.Namespace = None) -> None:
        """Initialize the terminal module with command line arguments.
        
        Args:
            args: Command line arguments namespace. Uses:
                - working_directory: Default working directory for commands
        """
        if args and hasattr(args, 'working_directory') and args.working_directory:
            self._current_working_directory = args.working_directory

    async def _run_command(self, command: str, cwd: Optional[str] = None) -> Dict[str, Any]:
        """Run a command and return its output and status.
        
        Args:
            command: The command to run
            cwd: Working directory for the command (optional)
            
        Returns:
            Dictionary containing:
                - stdout: Command output
                - stderr: Error output
                - returncode: Exit code
                - success: Boolean indicating if command succeeded
        """
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd or self._current_working_directory
            )
            
            stdout, stderr = await process.communicate()
            
            return {
                "stdout": stdout.decode() if stdout else "",
                "stderr": stderr.decode() if stderr else "",
                "returncode": process.returncode,
                "success": process.returncode == 0
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "returncode": 1,
                "success": False
            }

    def register_tools(self, mcp: FastMCP) -> None:
        """Register the terminal tools with the given MCP instance."""
        @mcp.tool()
        async def run_command(command: str, working_directory: str = "") -> Dict[str, Any]:
            """Run a command in the terminal and return its output.
            
            Args:
                command: The command to execute
                working_directory: Working directory for the command (default: current directory)
                
            Returns:
                Dictionary containing command output, error output, return code, and success status
            """
            return await self._run_command(command, working_directory if working_directory else None)

terminal_module = TerminalModule() 