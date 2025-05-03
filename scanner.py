import os # Handles file paths and directory operations
import csv # Handles the ouput in spreadsheet format
import argparse # Handles the user inputs from the command line

VERSION = "1.0.0" # Initial version of the tool

def bytes_to_mb(size_bytes):
    """Convert bytes to megabytes (rounded to two decimal places)."""
    return round(size_bytes / (1024 * 1024), 2)

def get_depth(start_path, current_path):
    """Calculate the folder depth relative to the starting path."""
    rel_path = os.path.relpath(current_path, start_path)
    return 0 if rel_path == '.' else rel_path.count(os.sep) + 1

def export_to_csv(file_list, filename):
    """Export the list of files to a CSV file."""
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Size_MB', 'File_Path'])
            for size_mb, file_path in file_list:
                writer.writerow([size_mb, file_path])
        print(f"\n✅ File data exported to: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"\n❌ Failed to write CSV: {e}")

def main():
    """Create a flexible command-line interface to control the scans."""
    parser = argparse.ArgumentParser(
        description="Scan a directory tree and report files based on filters.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('--version', action='version', version=f'%(prog)s v{VERSION}')
    parser.add_argument('--path', required=True, help='Root directory to scan')
    parser.add_argument('--min-size', type=float, default=0.0, help='Minimum file size in MB')
    parser.add_argument('--max-files', type=int, default=0, help='Maximum number of files to display (0 = unlimited)')
    parser.add_argument('--ext', type=str, default='', help='File extension filter (e.g., .mp3)')
    parser.add_argument('--name', type=str, default='', help='Filter files by name or suffix')
    parser.add_argument('--max-depth', type=int, default=0, help='Maximum folder depth (0 = no limit)')
    parser.add_argument('--export-csv', type=str, help='CSV output filename (optional)')

    args = parser.parse_args()

    path = os.path.abspath(os.path.expanduser(args.path))

    if not os.path.isdir(path):
        print("\nError: The specified directory does not exist or is not a folder.")
        return

    collected_files = []
    total_size_mb = 0

    for root, dirs, files in os.walk(path):
        current_depth = get_depth(path, root)
        if args.max_depth > 0 and current_depth > args.max_depth:
            dirs[:] = []
            continue

        for _file in files:
            try:
                full_path = os.path.join(root, _file)
                size_bytes = os.path.getsize(full_path)
                size_mb = bytes_to_mb(size_bytes)
                file_name = _file.lower()

                if size_mb < args.min_size:
                    continue
                if args.ext and not file_name.endswith(args.ext.lower()):
                    continue
                if args.name and args.name.lower() not in file_name:
                    continue

                collected_files.append((size_mb, full_path))
                total_size_mb += size_mb
            except (OSError, PermissionError):
                print(f"Skipped: {os.path.join(root, _file)} (access denied)")

    collected_files.sort(reverse=True, key=lambda x: x[0])

    displayed_files = collected_files[:args.max_files] if args.max_files > 0 else collected_files

    if displayed_files:
        print(f"\nFound {len(displayed_files)} matching files:\n")
        for size_mb, file_path in displayed_files:
            print(f"{size_mb} MB - {file_path}")
        print(f"\n📊 Total size of displayed files: {round(sum(f[0] for f in displayed_files), 2)} MB")
        print(f"📦 Total size of all matching files (before limit): {round(total_size_mb, 2)} MB")

        if args.export_csv:
            export_to_csv(displayed_files, args.export_csv)
    else:
        print("No files matched your criteria.")

if __name__ == '__main__':
    main()
