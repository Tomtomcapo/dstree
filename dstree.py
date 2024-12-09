#!/usr/bin/env python3

import os
import sys
import shutil
import argparse
from pathlib import Path
from typing import NamedTuple

class Colors:
    RESET = '\033[0m'
    
    @staticmethod
    def get_color(size_mb):
        if size_mb < 100: return '\033[38;2;0;255;0m'
        elif size_mb < 500: return '\033[38;2;255;255;0m'
        elif size_mb < 1024: return '\033[38;2;255;165;0m'
        else: return '\033[38;2;255;0;0m'
    
    USAGE_LOW = '\033[38;2;0;255;0m'
    USAGE_MED = '\033[38;2;255;255;0m'
    USAGE_HIGH = '\033[38;2;255;0;0m'

class FileInfo(NamedTuple):
    path: Path
    size: int
    is_dir: bool

def get_progress_bar(percentage, width=30):
    filled = int(width * percentage / 100)
    if percentage < 60:
        color = Colors.USAGE_LOW
    elif percentage < 85:
        color = Colors.USAGE_MED
    else:
        color = Colors.USAGE_HIGH
    
    bar = f"{color}{'█' * filled}{'░' * (width - filled)}{Colors.RESET}"
    return f"{bar} {percentage:5.1f}%"

def convert_size(size_bytes):
    size_mb = size_bytes / (1024 * 1024)
    color = Colors.get_color(size_mb)
    
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{color}{size_bytes:7.1f}{unit}{Colors.RESET}"
        size_bytes /= 1024.0

def format_entry(prefix, branch, name, size_str, progress=""):
    # Fixed widths for each column
    name_width = 45  # Width for the name column
    size_width = 10  # Width for the size number
    
    # Format the name part with fixed width
    name_part = f"{name:<{name_width}}"
    
    # Format the size part
    size_part = f"({size_str:>10})"
    
    # Combine all parts
    if progress:
        return f"{prefix}{branch}{name_part} {size_part}  {progress}"
    else:
        return f"{prefix}{branch}{name_part} {size_part}"

def get_dir_size(path):
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(file_path)
                except (OSError, FileNotFoundError):
                    continue
    except (OSError, PermissionError):
        return 0
    return total_size

def get_sorted_entries(path, threshold_bytes):
    entries = []
    for entry in path.iterdir():
        try:
            if entry.is_dir():
                size = get_dir_size(entry)
                if size > threshold_bytes:
                    entries.append(FileInfo(entry, size, True))
            else:
                size = entry.stat().st_size
                if size > threshold_bytes:
                    entries.append(FileInfo(entry, size, False))
        except (OSError, PermissionError):
            continue
    
    return sorted(entries, key=lambda x: x.size, reverse=True)


def print_tree(path, prefix="", is_last=True, threshold_bytes=0.2 * 1024 * 1024 * 1024, 
               current_depth=0, max_depth=None, parent_size=None):
    if max_depth is not None and current_depth > max_depth:
        return

    path = Path(path)
    current_dir_size = get_dir_size(path)
    
    if current_dir_size > threshold_bytes:
        if current_depth == 0:
            print(format_entry("", "", str(path) + "/", convert_size(current_dir_size)))
        else:
            branch = "└──" if is_last else "├──"
            percentage = (current_dir_size / parent_size) * 100
            print(format_entry(prefix, branch, path.name + "/", 
                             convert_size(current_dir_size), 
                             get_progress_bar(percentage)))
        
        if max_depth is not None and current_depth == max_depth:
            return

        new_prefix = prefix + ("    " if is_last else "│   ")
        entries = get_sorted_entries(path, threshold_bytes)
        
        for i, entry in enumerate(entries):
            is_last_entry = i == len(entries) - 1
            percentage = (entry.size / current_dir_size) * 100
            
            if entry.is_dir:
                print_tree(entry.path, new_prefix, is_last_entry, threshold_bytes,
                         current_depth + 1, max_depth, current_dir_size)
            else:
                file_branch = "└──" if is_last_entry else "├──"
                print(format_entry(new_prefix, file_branch, entry.path.name,
                                 convert_size(entry.size),
                                 get_progress_bar(percentage)))
            
            # Add connecting line after the last entry in a directory
            if is_last_entry and not is_last:
                indent = prefix + "│"
                print(f"{indent}")

def main():
    parser = argparse.ArgumentParser(description='Analyze directory sizes with visualization.')
    parser.add_argument('path', help='Directory path to analyze')
    parser.add_argument('--depth', type=int, help='Maximum depth to analyze (default: unlimited)',
                       default=None)
    parser.add_argument('--threshold', type=float, help='Size threshold in GB (default: 0.2)',
                       default=0.2)
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.path):
        print(f"Error: '{args.path}' is not a directory")
        sys.exit(1)
    
    total, used, free = shutil.disk_usage(args.path)
    disk_usage_percent = (used / total) * 100
    
    print(f"Disk Usage: {convert_size(used)}/{convert_size(total)} ({disk_usage_percent:.1f}%)")
    print(f"Free Space: {convert_size(free)}")
    print(get_progress_bar(disk_usage_percent, 40))
    print()
    
    print(f"Size threshold: {args.threshold}GB")
    print(f"Maximum depth: {'unlimited' if args.depth is None else args.depth}")
    print(f"Scanning directory: {args.path}")
    
    print("\nColor scale (sizes):")
    print(f"{Colors.get_color(50)}■{Colors.RESET} < 100MB")
    print(f"{Colors.get_color(250)}■{Colors.RESET} 100MB-500MB")
    print(f"{Colors.get_color(750)}■{Colors.RESET} 500MB-1GB")
    print(f"{Colors.get_color(1500)}■{Colors.RESET} > 1GB")
    
    print("\nColor scale (usage):")
    print(f"{Colors.USAGE_LOW}■{Colors.RESET} < 60%")
    print(f"{Colors.USAGE_MED}■{Colors.RESET} 60-85%")
    print(f"{Colors.USAGE_HIGH}■{Colors.RESET} > 85%")
    print("-" * 40)
    
    threshold_bytes = args.threshold * 1024 * 1024 * 1024
    print_tree(args.path, max_depth=args.depth, threshold_bytes=threshold_bytes)

if __name__ == "__main__":
    main()
  
