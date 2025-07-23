import os
import subprocess
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time
import platform

class ModPackBuilder:
    # Color scheme (Dark Theme)
    COLORS = {
        'bg': '#2d2d2d',
        'fg': '#e0e0e0',
        'accent': '#4CAF50',
        'text_bg': '#3d3d3d',
        'text_fg': '#ffffff',
        'button_bg': '#3d3d3d',
        'button_active': '#4CAF50',
        'entry_bg': '#3d3d3d',
        'entry_fg': '#ffffff',
        'progress_bg': '#3d3d3d',
        'progress_fg': '#4CAF50',
        'check_bg': '#2d2d2d',
        'check_fg': '#e0e0e0',
        'combobox_bg': '#3d3d3d',
        'combobox_fg': '#ffffff'
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Mod Pack Builder")
        self.root.geometry("800x720")
        self.is_building = False

        # Variables
        self.source_dir = tk.StringVar()
        self.dest_dir = tk.StringVar()
        self.pack_name = tk.StringVar(value="ModPack")
        self.archiver_path = tk.StringVar(value="7za.exe")
        self.use_compression = tk.BooleanVar(value=False)
        self.compression_level = tk.StringVar(value="-mx1")

        # Apply theme
        self.setup_theme()
        
        # GUI Elements
        self.setup_ui()

    def setup_theme(self):
        self.root.configure(bg=self.COLORS['bg'])
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=self.COLORS['bg'])
        style.configure('TLabel', background=self.COLORS['bg'], foreground=self.COLORS['fg'], font=('Arial', 10))
        style.configure('TButton', background=self.COLORS['button_bg'], foreground=self.COLORS['fg'], borderwidth=1, font=('Arial', 10))
        style.map('TButton', background=[('active', self.COLORS['button_active'])])
        style.configure('Build.TButton', background=self.COLORS['accent'], foreground='white', font=('Arial', 10, 'bold'))
        style.map('Build.TButton', background=[('active', self.COLORS['button_active'])])
        style.configure('Building.TButton', background='#2E7D32', foreground='white')
        style.configure('TEntry', fieldbackground=self.COLORS['entry_bg'], foreground=self.COLORS['entry_fg'], insertcolor=self.COLORS['entry_fg'], borderwidth=1)
        style.configure('TCombobox', fieldbackground=self.COLORS['combobox_bg'], foreground=self.COLORS['combobox_fg'], background=self.COLORS['combobox_bg'], selectbackground=self.COLORS['button_active'], selectforeground=self.COLORS['combobox_fg'], arrowcolor=self.COLORS['fg'])
        style.map('TCombobox',
                fieldbackground=[('readonly', self.COLORS['combobox_bg'])],
                background=[('readonly', self.COLORS['combobox_bg'])],
                selectbackground=[('readonly', self.COLORS['button_active'])],
                selectforeground=[('readonly', self.COLORS['combobox_fg'])])
        style.configure('Horizontal.TProgressbar', background=self.COLORS['progress_fg'], troughcolor=self.COLORS['progress_bg'], bordercolor=self.COLORS['bg'], lightcolor=self.COLORS['progress_fg'], darkcolor=self.COLORS['progress_fg'])

    def setup_ui(self):
        # Source Directory
        ttk.Label(self.root, text="Source Folder (with mods):").pack(pady=(10, 0))
        frame_source = ttk.Frame(self.root)
        frame_source.pack(fill=tk.X, padx=20, pady=5)
        self.source_entry = ttk.Entry(frame_source, textvariable=self.source_dir, width=70)
        self.source_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(frame_source, text="Browse", command=self.browse_source).pack(side=tk.RIGHT, padx=5)

        # Destination Directory
        ttk.Label(self.root, text="Destination Folder:").pack(pady=(10, 0))
        frame_dest = ttk.Frame(self.root)
        frame_dest.pack(fill=tk.X, padx=20, pady=5)
        self.dest_entry = ttk.Entry(frame_dest, textvariable=self.dest_dir, width=70)
        self.dest_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(frame_dest, text="Browse", command=self.browse_dest).pack(side=tk.RIGHT, padx=5)

        # Pack Name
        ttk.Label(self.root, text="Pack Name:").pack(pady=(10, 0))
        self.pack_entry = ttk.Entry(self.root, textvariable=self.pack_name)
        self.pack_entry.pack(fill=tk.X, padx=20, pady=5)

        # Archiver Path
        ttk.Label(self.root, text="Path to 7z:").pack(pady=(10, 0))
        frame_archiver = ttk.Frame(self.root)
        frame_archiver.pack(fill=tk.X, padx=20, pady=5)
        self.archiver_entry = ttk.Entry(frame_archiver, textvariable=self.archiver_path, width=70)
        self.archiver_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(frame_archiver, text="Browse", command=self.browse_archiver).pack(side=tk.RIGHT, padx=5)

        # Compression Options
        frame_compression = tk.Frame(self.root, bg=self.COLORS['bg'])
        frame_compression.pack(fill=tk.X, padx=20, pady=10)
        
        self.compression_check = tk.Checkbutton(
            frame_compression, 
            text="Enable Compression", 
            variable=self.use_compression,
            command=self.toggle_compression,
            bg=self.COLORS['check_bg'],
            fg=self.COLORS['check_fg'],
            selectcolor=self.COLORS['bg'],
            activebackground=self.COLORS['bg'],
            activeforeground=self.COLORS['fg'],
            font=('Arial', 10)
        )
        self.compression_check.pack(side=tk.LEFT)
        
        self.compression_menu = ttk.Combobox(
            frame_compression, 
            textvariable=self.compression_level, 
            values=["-mx1", "-mx3"],
            state="disabled", 
            width=10,
            style='TCombobox'
        )
        self.compression_menu.pack(side=tk.LEFT, padx=10)

        # Build Button and Progress Bar
        self.build_button = ttk.Button(self.root, text="Build", command=self.build_pack, style='Build.TButton')
        self.build_button.pack(pady=(20, 10))
        
        self.progress = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Log Console
        log_frame = ttk.Frame(self.root)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        # Log header with label and clear button
        log_header = ttk.Frame(log_frame)
        log_header.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(log_header, text="Log:").pack(side=tk.LEFT)
        
        clear_button = ttk.Button(
            log_header, 
            text="Clear Logs", 
            command=self.clear_logs,
            style='TButton'
        )
        clear_button.pack(side=tk.RIGHT)

        # Log text area with scrollbar
        log_container = ttk.Frame(log_frame)
        log_container.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_container, height=15, state=tk.DISABLED, 
                              bg=self.COLORS['text_bg'], fg=self.COLORS['text_fg'],
                              insertbackground=self.COLORS['text_fg'],
                              font=('Consolas', 9))
        scrollbar = ttk.Scrollbar(log_container)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)

    def clear_logs(self):
        """Clears the log window content"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.log("Logs cleared")

    def toggle_compression(self):
        if self.use_compression.get():
            self.compression_menu.config(state="readonly")
        else:
            self.compression_menu.config(state="disabled")

    def browse_source(self):
        dir_path = filedialog.askdirectory(title="Select Source Folder")
        if dir_path:
            self.source_dir.set(dir_path)
            self.log(f"Selected source folder: {dir_path}")

    def browse_dest(self):
        dir_path = filedialog.askdirectory(title="Select Destination Folder")
        if dir_path:
            self.dest_dir.set(dir_path)
            self.log(f"Selected destination folder: {dir_path}")

    def browse_archiver(self):
        file_path = filedialog.askopenfilename(title="Select 7z", filetypes=[("Executable", "*.exe")])
        if file_path:
            self.archiver_path.set(file_path)
            self.log(f"Selected archiver: {file_path}")

    def log(self, message):
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)
        self.root.update()

    def delete_folder(self, folder):
        try:
            self.log(f"Deleting folder: {folder}")
            
            if platform.system() == 'Windows':
                subprocess.run(f'rmdir /s /q "{folder}"', shell=True, check=True)
            else:
                subprocess.run(['rm', '-rf', folder], check=True)
                
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"Error deleting folder: {e}")
            return False

    def update_progress(self, value, maximum=None):
        if maximum:
            self.progress.config(maximum=maximum)
        self.progress['value'] = value
        self.root.update()

    def build_pack(self):
        if self.is_building:
            return
            
        self.is_building = True
        self.build_button.config(text="Building...", style='Building.TButton')
        self.progress['value'] = 0
        self.root.update()

        try:
            # Validate inputs
            source = self.source_dir.get()
            if not source:
                messagebox.showerror("Error", "Source folder is not selected!")
                return

            dest = self.dest_dir.get() or "."
            pack_name = self.pack_name.get()
            archiver = self.archiver_path.get()

            if not os.path.exists(archiver):
                messagebox.showerror("Error", f"Archiver not found: {archiver}")
                return

            # Start build process
            self.log("\n=== Building Mod Pack ===")
            self.log(f"Source: {source}")
            self.log(f"Destination: {dest}")
            self.log(f"Pack Name: {pack_name}")
            self.log(f"Archiver: {archiver}")
            
            if self.use_compression.get():
                self.log(f"Compression: {self.compression_level.get()}")
            else:
                self.log("Compression: Disabled (store only)")

            # List mods in source
            try:
                mods = [d for d in os.listdir(source) if os.path.isdir(os.path.join(source, d))]
                self.log("\nFound mods:")
                for mod in mods:
                    self.log(f"- {mod}")
            except Exception as e:
                self.log(f"\nError listing mods: {str(e)}")
                messagebox.showerror("Error", f"Cannot list mods in source folder:\n{str(e)}")
                return

            # Create temp folder
            temp_folder = os.path.join(dest, pack_name)
            if os.path.exists(temp_folder):
                if not self.delete_folder(temp_folder):
                    messagebox.showerror("Error", f"Could not delete existing temp folder:\n{temp_folder}\n\n"
                                                "Please close any programs using it and try again.")
                    return

            try:
                os.makedirs(temp_folder)
                self.log(f"\nCreated temp folder: {temp_folder}")
            except Exception as e:
                self.log(f"\nError creating temp folder: {str(e)}")
                messagebox.showerror("Error", f"Cannot create temp folder:\n{str(e)}")
                return

            # Copy files recursively
            self.log("\nCopying files...")
            total_files = 0
            
            # First count all files for progress
            file_count = 0
            for mod in mods:
                mod_path = os.path.join(source, mod)
                for root, dirs, files in os.walk(mod_path):
                    file_count += len(files)
            
            self.update_progress(0, file_count)
            current_progress = 0

            for mod in mods:
                mod_path = os.path.join(source, mod)
                try:
                    for root, dirs, files in os.walk(mod_path):
                        for file in files:
                            src_file = os.path.join(root, file)
                            rel_path = os.path.relpath(src_file, mod_path)
                            dest_file = os.path.join(temp_folder, rel_path)
                            
                            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                            shutil.copy2(src_file, dest_file)
                            total_files += 1
                            current_progress += 1
                            
                            if total_files % 10 == 0:
                                self.update_progress(current_progress)
                                self.log(f"Copied {total_files} of {file_count} files...")
                except Exception as e:
                    self.log(f"\nError copying from {mod}: {str(e)}")
                    continue

            self.log(f"\nTotal files copied: {total_files}")
            self.update_progress(file_count)

            # Build archive
            archive_path = os.path.join(dest, f"{pack_name}.7z")
            if os.path.exists(archive_path):
                self.log("\nDeleting old archive...")
                try:
                    os.remove(archive_path)
                except Exception as e:
                    self.log(f"\nError deleting old archive: {str(e)}")
                    messagebox.showerror("Error", f"Cannot delete old archive:\n{str(e)}")
                    return

            self.log("\nCreating archive...")
            cmd = [archiver, "a"]
            
            if self.use_compression.get():
                cmd.extend([self.compression_level.get(), "-ssp", "-stl", "-y"])
            else:
                cmd.extend(["-mx0", "-ssp", "-stl", "-y"])
            
            cmd.extend([archive_path, os.path.join(temp_folder, "*")])
            
            self.log("Command: " + " ".join(cmd))
            
            try:
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                         universal_newlines=True, shell=True)
                
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.log(output.strip())
                
                if process.returncode != 0:
                    error = process.stderr.read()
                    self.log(f"\nArchive creation failed:\n{error}")
                    messagebox.showerror("Error", "Failed to create archive!")
                    return
                    
                archive_size = os.path.getsize(archive_path) / (1024 * 1024)
                self.log(f"\nSuccessfully created archive: {archive_path}")
                self.log(f"Archive size: {archive_size:.2f} MB")
            except Exception as e:
                self.log(f"\nError during archive creation: {str(e)}")
                messagebox.showerror("Error", f"Archive creation failed:\n{str(e)}")
                return

            # Cleanup
            self.log("\nCleaning up temp folder...")
            if not self.delete_folder(temp_folder):
                self.log("Warning: Could not completely delete temp folder")

            self.log("\n=== Operation completed ===")
            
        finally:
            self.is_building = False
            self.build_button.config(text="Build", style='Build.TButton')
            self.progress['value'] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = ModPackBuilder(root)
    root.mainloop()