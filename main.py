import os
import csv

def bytes_to_mb(size_bytes):
    """Convert bytes to megabytes, rounded to two decimal places."""
    return round(size_bytes / (1024 * 1024), 2)

def get_depth(start_path, current_path):
    """
    Calculate the folder depth relative to the starting path.
    Example:
        If start_path is /A and current_path is /A/B/C, depth = 2
    """
    rel_path = os.path.relpath(current_path, start_path)
    return 0 if rel_path == '.' else rel_path.count(os.sep) + 1

def export_to_csv(file_list, filename='file_report.csv'):
    """
    Export the list of files to a CSV file.
    :param file_list: List of tuples (size_mb, file_path)
    :param filename: Output CSV filename
    """
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Size_MB', 'File_Path'])  # Header
            for size_mb, file_path in file_list:
                writer.writerow([size_mb, file_path])
        print(f"\n✅ File data exported to: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"\n❌ Failed to write CSV: {e}")

def main():
    # Step 1: Greet the user and prompt for a starting directory
    print("Welcome to the File System Traverser! 🚀")
    print("\nEnter a valid directory path.")
    print(" - Absolute paths: /Users/Name/Documents or C:\\Users\\Name\\Documents")

    # Step 2: Get and sanitize the directory input
    user_path = input("\nEnter the directory path: ").strip()
    path = os.path.abspath(os.path.expanduser(user_path))

    # Step 3: Validate the directory
    if not os.path.isdir(path):
        print("\nError: The specified directory does not exist or is not a folder.")
        return

    # Step 4: Prompt for size filter (MB)
    try:
        min_size_mb = float(input("Only show files larger than how many MB? (e.g., 1.5): ").strip())
    except ValueError:
        print("Invalid number. Defaulting to 0 MB.")
        min_size_mb = 0

    # Step 5: Prompt for maximum number of files to display
    try:
        max_files = int(input("Maximum number of files to display? (Enter 0 for unlimited): ").strip())
    except ValueError:
        print("Invalid number. Defaulting to unlimited.")
        max_files = 0

    # Step 6: Prompt for file extension filter (case-insensitive)
    ext_filter = input("Filter by file extension? (e.g., .mp3) Leave blank for all: ").strip().lower()

    # Step 7: Prompt for file name substring or suffix
    name_filter = input("Filter files by name or suffix? (e.g., report, _backup) Leave blank for all: ").strip().lower()

    # Step 8: Prompt for recursive depth limit
    try:
        max_depth = int(input("Maximum folder depth? (0 = no limit): ").strip())
    except ValueError:
        print("Invalid number. Defaulting to no limit.")
        max_depth = 0

    # Step 9: Traverse directory and collect matching files
    collected_files = []      # List of (size_mb, file_path)
    total_size_mb = 0         # Total size of all matches (even those not shown)

    print(f"\nScanning directory: {path} ...\n")

    for root, dirs, files in os.walk(path):
        # Determine how deep we are in the directory tree
        current_depth = get_depth(path, root)

        # If current depth exceeds limit, do not recurse further into subfolders
        if max_depth > 0 and current_depth > max_depth:
            dirs[:] = []  # Clear the list to prevent further traversal
            continue

        for _file in files:
            try:
                full_path = os.path.join(root, _file)
                size_bytes = os.path.getsize(full_path)
                size_mb = bytes_to_mb(size_bytes)
                file_name = _file.lower()

                # Apply all filters
                if size_mb < min_size_mb:
                    continue
                if ext_filter and not file_name.endswith(ext_filter):
                    continue
                if name_filter and name_filter not in file_name:
                    continue

                collected_files.append((size_mb, full_path))
                total_size_mb += size_mb

            except (OSError, PermissionError):
                # Skip files we don't have permission to access
                print(f"Skipped: {os.path.join(root, _file)} (access denied)")

    # Step 10: Sort files by size, descending
    collected_files.sort(reverse=True, key=lambda x: x[0])

    # Step 11: Limit displayed results if max_files is set
    displayed_files = collected_files[:max_files] if max_files > 0 else collected_files

    # Step 12: Display results to user
    if displayed_files:
        print(f"Found {len(displayed_files)} matching files:\n")
        for size_mb, file_path in displayed_files:
            print(f"{size_mb} MB - {file_path}")
        print(f"\n📊 Total size of displayed files: {round(sum(f[0] for f in displayed_files), 2)} MB")
        print(f"📦 Total size of all matching files (before display limit): {round(total_size_mb, 2)} MB")

        # Step 13: Ask user if they want to export to CSV
        save_csv = input("\nDo you want to export the results to CSV? (y/n): ").strip().lower()
        if save_csv == 'y':
            export_to_csv(displayed_files)
    else:
        print("No files matched your criteria.")

if __name__ == '__main__':
    main()
