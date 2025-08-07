#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division
import os
import sys

if sys.version_info[0] == 3:
    import math
    input_func = input
else:
    import math
    input_func = raw_input

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'

def colored_print(text, color=Colors.WHITE, bold=False, bg_color=None):
    """Print text dengan warna"""
    if os.name == 'nt':  
        try:
            import colorama
            colorama.init()
        except ImportError:
            print(text)
            return
    
    output = ""
    if bg_color:
        output += bg_color
    if bold:
        output += Colors.BOLD
    output += color + text + Colors.RESET
    print(output)

def print_header(text):
    """Print header dengan style khusus"""
    colored_print("=" * len(text), Colors.CYAN, bold=True)
    colored_print(text, Colors.CYAN, bold=True)
    colored_print("=" * len(text), Colors.CYAN, bold=True)

def print_success(text):
    """Print pesan sukses"""
    colored_print("✓ " + text, Colors.GREEN, bold=True)

def print_info(text):
    """Print informasi"""
    colored_print("ℹ " + text, Colors.BLUE)

def print_warning(text):
    """Print peringatan"""
    colored_print("⚠ " + text, Colors.YELLOW, bold=True)

def print_error(text):
    """Print error"""
    colored_print("✗ " + text, Colors.RED, bold=True)

def print_progress(text):
    """Print progress"""
    colored_print("→ " + text, Colors.MAGENTA)

class TextSplitter:
    def __init__(self, input_file):
        self.input_file = input_file
        self.file_size = os.path.getsize(input_file)
        
    def _get_base_name(self, filepath):
        """Ekstrak nama file tanpa ekstensi"""
        basename = os.path.basename(filepath)
        name_without_ext = os.path.splitext(basename)[0]
        extension = os.path.splitext(basename)[1]
        return name_without_ext, extension
    
    def _get_unique_filename(self, filename):
        """Generate unique filename jika file sudah ada"""
        if not os.path.exists(filename):
            return filename
            
        base_name, extension = os.path.splitext(filename)
        counter = 1
        
        while True:
            new_filename = "{}({}){}".format(base_name, counter, extension)
            if not os.path.exists(new_filename):
                print_warning("File {} sudah ada, menggunakan {}".format(filename, new_filename))
                return new_filename
            counter += 1
            
            if counter > 9999:
                print_error("Terlalu banyak file dengan nama serupa!")
                return "{}({}){}".format(base_name, counter, extension)
        
    def split_by_lines(self, lines_per_file=1000):
        """Split file berdasarkan jumlah baris"""
        base_name, extension = self._get_base_name(self.input_file)
        
        print_info("Memulai split berdasarkan jumlah baris...")
        
        encoding = 'utf-8'
        try:
            with open(self.input_file, 'r', encoding=encoding) as test_file:
                test_file.read(100)
        except (TypeError, UnicodeDecodeError):
            encoding = None
        
        if encoding:
            # Python 3
            input_file = open(self.input_file, 'r', encoding=encoding)
        else:
            # Python 2
            input_file = open(self.input_file, 'r')
            
        try:
            file_num = 1
            line_count = 0
            current_file = None
            
            for line in input_file:
                if line_count % lines_per_file == 0:
                    if current_file:
                        current_file.close()
                    
                    output_name = "{}_part{:03d}{}".format(base_name, file_num, extension)
                    output_name = self._get_unique_filename(output_name)
                    
                    if encoding:
                        # Python 3
                        current_file = open(output_name, 'w', encoding=encoding)
                    else:
                        # Python 2
                        current_file = open(output_name, 'w')
                    
                    print_progress("Membuat file: {}".format(
                        colored_text(output_name, Colors.CYAN)))
                    file_num += 1
                
                current_file.write(line)
                line_count += 1
            
            if current_file:
                current_file.close()
                
        finally:
            input_file.close()
        
        print_success("File berhasil dipecah menjadi {} bagian!".format(file_num-1))
        return file_num - 1

    def split_by_size(self, size_mb=10):
        """Split file berdasarkan ukuran (MB)"""
        base_name, extension = self._get_base_name(self.input_file)
        chunk_size = int(size_mb * 1024 * 1024)  
        
        print_info("Memulai split berdasarkan ukuran file...")
        
        encoding = 'utf-8'
        try:
            with open(self.input_file, 'r', encoding=encoding) as test_file:
                test_file.read(100)
        except (TypeError, UnicodeDecodeError):
            encoding = None
        
        if encoding:
            input_file = open(self.input_file, 'r', encoding=encoding)
        else:
            input_file = open(self.input_file, 'r')
            
        try:
            file_num = 1
            current_size = 0
            current_content = []
            
            for line in input_file:
                if sys.version_info[0] == 3:
                    line_size = len(line.encode('utf-8'))
                else:
                    line_size = len(line.encode('utf-8') if isinstance(line, unicode) else line)
                
                if current_size + line_size > chunk_size and current_content:
                    output_name = "{}_part{:03d}{}".format(base_name, file_num, extension)
                    output_name = self._get_unique_filename(output_name)
                    
                    if encoding:
                        out_file = open(output_name, 'w', encoding=encoding)
                    else:
                        out_file = open(output_name, 'w')
                    
                    try:
                        for content_line in current_content:
                            out_file.write(content_line)
                    finally:
                        out_file.close()
                    
                    colored_print("→ Membuat file: {} ({:.2f} MB)".format(
                        colored_text(output_name, Colors.CYAN),
                        current_size/1024.0/1024.0), Colors.MAGENTA)
                    
                    current_content = []
                    current_size = 0
                    file_num += 1
                
                current_content.append(line)
                current_size += line_size
            
            if current_content:
                output_name = "{}_part{:03d}{}".format(base_name, file_num, extension)
                output_name = self._get_unique_filename(output_name)
                
                if encoding:
                    out_file = open(output_name, 'w', encoding=encoding)
                else:
                    out_file = open(output_name, 'w')
                
                try:
                    for content_line in current_content:
                        out_file.write(content_line)
                finally:
                    out_file.close()
                    
                colored_print("→ Membuat file: {} ({:.2f} MB)".format(
                    colored_text(output_name, Colors.CYAN),
                    current_size/1024.0/1024.0), Colors.MAGENTA)
                    
        finally:
            input_file.close()
        
        print_success("File berhasil dipecah menjadi {} bagian!".format(file_num))
        return file_num

    def split_by_parts(self, num_parts=5):
        """Split file menjadi jumlah bagian yang ditentukan"""
        base_name, extension = self._get_base_name(self.input_file)
        
        print_info("Memulai split menjadi {} bagian...".format(num_parts))
        
        encoding = 'utf-8'
        try:
            with open(self.input_file, 'r', encoding=encoding) as test_file:
                test_file.read(100)
        except (TypeError, UnicodeDecodeError):
            encoding = None
        
        print_info("Menghitung total baris...")
        if encoding:
            count_file = open(self.input_file, 'r', encoding=encoding)
        else:
            count_file = open(self.input_file, 'r')
            
        try:
            total_lines = sum(1 for _ in count_file)
        finally:
            count_file.close()
        
        lines_per_file = int(math.ceil(total_lines / float(num_parts)))
        print_info("Baris per file: {}".format(lines_per_file))
        
        if encoding:
            input_file = open(self.input_file, 'r', encoding=encoding)
        else:
            input_file = open(self.input_file, 'r')
            
        try:
            part = 0
            for part in range(num_parts):
                output_name = "{}_part{:03d}{}".format(base_name, part+1, extension)
                output_name = self._get_unique_filename(output_name)
                lines_written = 0
                
                if encoding:
                    out_file = open(output_name, 'w', encoding=encoding)
                else:
                    out_file = open(output_name, 'w')
                
                try:
                    while lines_written < lines_per_file:
                        line = input_file.readline()
                        if not line:  
                            break
                        out_file.write(line)
                        lines_written += 1
                finally:
                    out_file.close()
                
                if lines_written > 0:
                    colored_print("→ Membuat file: {} ({:,} baris)".format(
                        colored_text(output_name, Colors.CYAN), lines_written), Colors.MAGENTA)
                else:
                    try:
                        os.remove(output_name)
                    except OSError:
                        pass
                    break
                    
        finally:
            input_file.close()
        
        print_success("File berhasil dipecah menjadi {} bagian!".format(part+1))
        return part + 1

    def get_file_info(self):
        """Menampilkan informasi file"""
        encoding = 'utf-8'
        try:
            with open(self.input_file, 'r', encoding=encoding) as test_file:
                test_file.read(100)
        except (TypeError, UnicodeDecodeError):
            encoding = None
        
        print_info("Menganalisis file...")
        
        if encoding:
            count_file = open(self.input_file, 'r', encoding=encoding)
        else:
            count_file = open(self.input_file, 'r')
            
        try:
            line_count = sum(1 for _ in count_file)
        finally:
            count_file.close()
        
        size_mb = self.file_size / (1024.0 * 1024.0)
        
        print("")
        colored_print("File: {}".format(self.input_file), Colors.WHITE, bold=True)
        colored_print("Ukuran: {:.2f} MB ({:,} bytes)".format(size_mb, self.file_size), Colors.YELLOW)
        colored_print("Total baris: {:,}".format(line_count), Colors.GREEN)
        print("")
        
        return line_count, size_mb

def colored_text(text, color):
    """Return colored text string"""
    if os.name == 'nt':  
        try:
            import colorama
            colorama.init()
            return color + text + Colors.RESET
        except ImportError:
            return text
    return color + text + Colors.RESET

def show_menu():
    print("")
    colored_print("PILIH METODE SPLIT:", Colors.WHITE, bold=True)
    print("")
    colored_print("( 1 ) Split berdasarkan jumlah baris", Colors.CYAN)
    colored_print("( 2 ) Split berdasarkan ukuran file (MB)", Colors.BLUE) 
    colored_print("( 3 ) Split menjadi jumlah bagian tertentu", Colors.MAGENTA)
    print("")

def main():
    print_header("{ • } TEXT SPLITTER { • }")
    print("")
    
    colored_print("[ x ] Masukkan nama file .txt: [ x ]", Colors.WHITE, bold=True)
    input_file = input_func("» ").strip()
    
    if not os.path.exists(input_file):
        print_error("File tidak ditemukan!")
        return
    
    print_success("File ditemukan!")
    
    splitter = TextSplitter(input_file)
    
    colored_print("\n INFORMASI FILE:", Colors.WHITE, bold=True)
    splitter.get_file_info()
    
    show_menu()
    
    colored_print("Masukkan pilihan Anda:", Colors.WHITE, bold=True)
    choice = input_func("» ").strip()
    
    print("")
    
    if choice == "1":
        colored_print("Jumlah baris per file (default 1000):", Colors.YELLOW)
        lines_input = input_func("» ") or "1000"
        lines = int(lines_input)
        splitter.split_by_lines(lines)
        
    elif choice == "2":
        colored_print("Ukuran per file dalam MB (default 10):", Colors.YELLOW)
        size_input = input_func("» ") or "10"
        size = float(size_input)
        splitter.split_by_size(size)
        
    elif choice == "3":
        colored_print("Jumlah bagian (default 5):", Colors.YELLOW)
        parts_input = input_func("» ") or "5"
        parts = int(parts_input)
        splitter.split_by_parts(parts)
        
    else:
        print_error("Pilihan tidak valid!")
        return
    
    print("")
    colored_print("PROSES SELESAI!", Colors.GREEN, bold=True, bg_color=Colors.BG_GREEN)

if __name__ == "__main__":
    main()