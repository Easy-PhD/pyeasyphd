import os
import re
from pathlib import Path


class LaTeXImportMerger:
    r"""Merges LaTeX files by recursively expanding \input, \import, and \include commands.

    This class processes LaTeX files and replaces inclusion commands with the actual
    content of the referenced files, preserving proper directory context for relative
    path resolution.

    Attributes:
        encoding (str): Character encoding for reading and writing files.
        processed_files (set): Tracks processed files to avoid circular dependencies.
        verbose (bool): If True, prints detailed processing information.

    Example:
        >>> merger = LaTeXImportMerger()
        >>> output_path = merger.merge_latex_file("main.tex", "complete.tex")
        >>> files = merger.find_all_imports("main.tex")
    """

    def __init__(self, encoding: str = "utf-8") -> None:
        """Initializes the LaTeX import merger.

        Args:
            encoding: Character encoding for file operations (default: 'utf-8').
        """
        self.encoding = encoding
        self.processed_files = set()
        self.verbose = True

    def merge_latex_file(
        self,
        main_file_path: str | Path,
        output_file_path: str | Path | None = None,
    ) -> str:
        r"""Merges a main LaTeX file with all its nested input/import files.

        Recursively processes \input{}, \import{}, and \include{} commands,
        replacing them with the content of referenced files while preserving
        directory context for relative path resolution.

        Args:
            main_file_path: Path to the main LaTeX file to process.
            output_file_path: Path for the merged output file. If None, a filename
                with "_merged" suffix will be generated automatically.

        Returns:
            The path to the merged output file.

        Raises:
            FileNotFoundError: If the main file does not exist.
        """
        main_file_path = Path(main_file_path).resolve()

        if not main_file_path.exists():
            raise FileNotFoundError(f"Main file not found: {main_file_path}")

        # Generate output filename if not provided.
        if output_file_path is None:
            output_dir = main_file_path.parent
            output_name = main_file_path.stem + "_merged" + main_file_path.suffix
            output_file_path = output_dir / output_name
        else:
            output_file_path = Path(output_file_path)

        print(f"Processing main file: {main_file_path}")
        print(f"Output file: {output_file_path}")

        # Clear processed files tracking for new merge operation.
        self.processed_files.clear()

        # Process the main file starting from its parent directory as base.
        merged_content = self._process_file(main_file_path, main_file_path.parent)

        # Write the merged content to output file.
        with open(output_file_path, "w", encoding=self.encoding) as f:
            f.write(merged_content)

        print(f"\n✅ Merge completed! Processed {len(self.processed_files)} files")
        print(f"Output file: {output_file_path}")

        return str(output_file_path)

    def _process_file(self, file_path: Path, current_base_dir: Path) -> str:
        r"""Processes a single LaTeX file, handling nested import commands.

        Reads the file, identifies \input, \import, and \include commands,
        and recursively replaces them with file contents. Tracks processed
        files to prevent circular dependencies.

        Args:
            file_path: Absolute path to the file to process.
            current_base_dir: Base directory for resolving relative paths in
                this file context.

        Returns:
            Processed file content with imports replaced.

        Note:
            - Adds warning comments for circular dependencies.
            - Preserves original file structure in comments.
            - Maintains proper directory context for nested imports.
        """
        file_path_str = str(file_path.resolve())

        # Check for circular dependencies.
        if file_path_str in self.processed_files:
            print(f"⚠️  Warning: File {file_path} already processed, skipping")
            return f"% Warning: File {file_path} already included, skipping\n"

        self.processed_files.add(file_path_str)

        if self.verbose:
            print(f"  Processing: {file_path} (base directory: {current_base_dir})")

        # Read file content.
        try:
            with open(file_path, "r", encoding=self.encoding) as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error: Cannot read file {file_path}: {e}")
            return f"% Error: Cannot read file {file_path}: {e}\n"

        # Process all import commands in sequence.
        processed_content = content
        processed_content = self._replace_input_commands(processed_content, current_base_dir)
        processed_content = self._replace_import_commands(processed_content, current_base_dir)
        processed_content = self._replace_include_commands(processed_content, current_base_dir)

        return processed_content

    def _replace_input_commands(self, content: str, base_dir: Path) -> str:
        r"""Replaces \input{} commands with file contents.

        Args:
            content: LaTeX content containing \input commands.
            base_dir: Base directory for resolving relative file paths.

        Returns:
            Content with \input commands replaced by file contents.

        Note:
            - \input maintains the same base directory for nested paths.
            - Supports both \input{file} and \input file syntax.
            - Adds delimiting comments for clarity in merged output.
        """
        # Regex pattern for \input commands with optional braces.
        input_pattern = r"\\input\s*(?:\{([^}]+)\}|([^\s\{]+))"

        def replace_input(match: re.Match) -> str:
            r"""Callback function to replace a single \input command.

            Args:
                match: Regex match object for the \input command.

            Returns:
                The replacement string with file contents or error message.
            """
            # Extract filename from either group 1 (braced) or group 2 (unbraced).
            filename = (match.group(1) or match.group(2)).strip().strip('"').strip("'")

            # Find the referenced file.
            file_path = self._find_file(filename, base_dir)

            if file_path is None:
                error_msg = f"% Error: Input file not found: {filename}"
                print(f"❌ {error_msg}")
                return error_msg + "\n"

            # For \input, nested files use the same base directory.
            replacement = f"\n% ====== Start input: {filename} ======\n"
            replacement += f"% Original file: {file_path}\n"
            replacement += f"% Base directory: {base_dir}\n"
            replacement += self._process_file(file_path, base_dir)
            replacement += f"\n% ====== End input: {filename} ======\n"

            return replacement

        return re.sub(input_pattern, replace_input, content)

    def _replace_import_commands(self, content: str, base_dir: Path) -> str:
        r"""Replaces \import{path}{file} commands with file contents.

        Args:
            content: LaTeX content containing \import commands.
            base_dir: Current base directory for path resolution.

        Returns:
            Content with \import commands replaced by file contents.

        Note:
            - \import changes the base directory for nested relative paths.
            - Format: \import{path}{filename}
            - The imported file's relative paths are resolved relative to 'path'.
        """
        # Regex pattern for \import{path}{file} commands.
        import_pattern = r"\\import\s*\{([^}]+)\}\s*\{([^}]+)\}"

        def replace_import(match: re.Match) -> str:
            r"""Callback function to replace a single \import command.

            Args:
                match: Regex match object for the \import command.

            Returns:
                The replacement string with file contents or error message.
            """
            import_path = match.group(1).strip().strip('"').strip("'")
            filename = match.group(2).strip().strip('"').strip("'")

            # Construct the import directory path.
            import_dir = Path(base_dir) / import_path

            # Find the referenced file in the import directory.
            file_path = self._find_file(filename, import_dir)

            if file_path is None:
                error_msg = f"% Error: Import file not found: {import_path}/{filename}"
                print(f"❌ {error_msg}")
                return error_msg + "\n"

            # For \import, nested files use the import directory as base.
            replacement = f"\n% ====== Start import: {import_path}/{filename} ======\n"
            replacement += f"% Original file: {file_path}\n"
            replacement += f"% New base directory: {import_dir}\n"
            replacement += self._process_file(file_path, import_dir)
            replacement += f"\n% ====== End import: {import_path}/{filename} ======\n"

            return replacement

        return re.sub(import_pattern, replace_import, content)

    def _replace_include_commands(self, content: str, base_dir: Path) -> str:
        r"""Replaces \include{} and \includeonly{} commands with file contents.

        Args:
            content: LaTeX content containing \include commands.
            base_dir: Base directory for resolving relative file paths.

        Returns:
            Content with \include commands replaced by file contents.

        Note:
            - \include is similar to \input but with page break semantics.
            - \includeonly is for selective inclusion during compilation.
            - In merged output, page break behavior may need manual adjustment.
        """
        # Regex pattern for \include and \includeonly commands.
        include_pattern = r"\\include(?:only)?\s*\{([^}]+)\}"

        def replace_include(match: re.Match) -> str:
            r"""Callback function to replace a single \include command.

            Args:
                match: Regex match object for the \include command.

            Returns:
                The replacement string with file contents or error message.
            """
            filename = match.group(1).strip().strip('"').strip("'")

            # Find the referenced file.
            file_path = self._find_file(filename, base_dir)

            if file_path is None:
                error_msg = f"% Error: Include file not found: {filename}"
                print(f"❌ {error_msg}")
                return error_msg + "\n"

            # \include maintains the same base directory like \input.
            replacement = f"\n% ====== Start include: {filename} ======\n"
            replacement += "% Note: \\include forces page breaks, may need adjustment\n"
            replacement += f"% Original file: {file_path}\n"
            replacement += self._process_file(file_path, base_dir)
            replacement += f"\n% ====== End include: {filename} ======\n"

            return replacement

        return re.sub(include_pattern, replace_include, content)

    def _find_file(self, filename: str, search_dir: Path) -> Path | None:
        """Locates a file with various extensions in the specified directory.

        Args:
            filename: Name of the file to find (with or without extension).
            search_dir: Directory to search for the file.

        Returns:
            Resolved path to the file if found, None otherwise.

        Note:
            - Tries absolute path first if filename is absolute.
            - Attempts common LaTeX extensions: .tex, .sty, .cls, .bib.
            - Also tries filename without additional extension.
        """
        # Check if filename is an absolute path.
        if Path(filename).is_absolute():
            if Path(filename).exists():
                return Path(filename).resolve()

        # Common LaTeX file extensions to try.
        extensions = [".tex", ""]

        for ext in extensions:
            # Try filename with extension appended.
            test_path = search_dir / (filename + ext)
            if test_path.exists():
                return test_path.resolve()

            # Try filename as-is (may already have extension).
            test_path = search_dir / filename
            if test_path.exists():
                return test_path.resolve()

        return None

    def find_all_imports(self, main_file_path: str | Path) -> list[tuple]:
        """Discovers all files referenced by import commands without merging.

        Args:
            main_file_path: Path to the main LaTeX file.

        Returns:
            List of (file_path, base_dir, import_type) tuples for all discovered files.

        Note:
            - Useful for analyzing project structure before merging.
            - Shows import method (input, import, or direct) for each file.
            - Displays relative paths for clarity.
        """
        main_file_path = Path(main_file_path).resolve()

        files_info = []  # List of (file_path, base_dir, import_method)

        def _find_in_file(file_path: Path, base_dir: Path, processed: set) -> None:
            """Recursive helper function to find imports in a file.

            Args:
                file_path: File to analyze.
                base_dir: Base directory for this file's context.
                processed: Set of processed (file_path, base_dir) pairs to avoid cycles.
            """
            # Create unique key for this file in its directory context.
            file_key = (str(file_path.resolve()), str(base_dir))
            if file_key in processed:
                return

            processed.add(file_key)
            files_info.append((file_path, base_dir, "direct"))

            try:
                with open(file_path, "r", encoding=self.encoding) as f:
                    content = f.read()
            except Exception as e:
                print(e)
                return

            # Find all \input commands.
            input_pattern = r"\\input\s*(?:\{([^}]+)\}|([^\s\{]+))"
            for match in re.finditer(input_pattern, content):
                filename = (match.group(1) or match.group(2)).strip().strip('"').strip("'")
                found = self._find_file(filename, base_dir)
                if found:
                    _find_in_file(found, base_dir, processed)

            # Find all \import commands.
            import_pattern = r"\\import\s*\{([^}]+)\}\s*\{([^}]+)\}"
            for match in re.finditer(import_pattern, content):
                import_path = match.group(1).strip().strip('"').strip("'")
                filename = match.group(2).strip().strip('"').strip("'")
                import_dir = Path(base_dir) / import_path
                found = self._find_file(filename, import_dir)
                if found:
                    _find_in_file(found, import_dir, processed)

        # Start recursive discovery from main file.
        _find_in_file(main_file_path, main_file_path.parent, set())

        # Display results.
        print(f"Found {len(files_info)} related files:")
        for i, (file_path, base_dir, import_type) in enumerate(files_info, 1):
            rel_path = os.path.relpath(file_path, main_file_path.parent)
            print(f"  {i:3d}. {rel_path}")
            print(f"       Base directory: {os.path.relpath(base_dir, main_file_path.parent)}")
            print(f"       Import method: {import_type}")

        return files_info
