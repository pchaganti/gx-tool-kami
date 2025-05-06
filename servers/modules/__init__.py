from typing import Protocol, Dict, Any, Optional, runtime_checkable
import argparse
from mcp.server.fastmcp import FastMCP

@runtime_checkable
class MCPModule(Protocol):
    def register_tools(self, mcp: FastMCP) -> None:
        """Register this module's tools with the given MCP instance."""
        ...
    
    def initialize(self, args: argparse.Namespace = None) -> None:
        """Initialize the module with command line arguments."""
        ...
    
    def register_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Register command line arguments for this module.
        
        Args:
            parser: The argument parser to add arguments to.
        """
        ... 