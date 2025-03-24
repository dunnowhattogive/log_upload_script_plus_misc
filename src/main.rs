use clap::{Arg, Command};
use eframe::{egui, epi};
use native_dialog::FileDialog;
use std::process::Command as ProcessCommand;

fn main() {
    let options = eframe::NativeOptions::default();
    eframe::run_native(
        "Rust Frontend GUI",
        options,
        Box::new(|_cc| Box::new(MyApp::default())),
    );
}

struct MyApp {
    directory: String,
    yearly: bool,
    battery_test: bool,
}

impl Default for MyApp {
    fn default() -> Self {
        Self {
            directory: String::new(),
            yearly: false,
            battery_test: false,
        }
    }
}

impl epi::App for MyApp {
    fn name(&self) -> &str {
        "Rust Frontend GUI"
    }

    fn update(&mut self, ctx: &egui::CtxRef, _frame: &epi::Frame) {
        egui::CentralPanel::default().show(ctx, |ui| {
            ui.heading("Rust Frontend for Python SMB Upload Script");

            if ui.button("Select Directory").clicked() {
                if let Some(path) = FileDialog::new().show_open_single_dir().ok().flatten() {
                    self.directory = path.to_string_lossy().to_string();
                }
            }

            ui.label(format!("Selected Directory: {}", self.directory));

            ui.checkbox(&mut self.yearly, "Aggregate data by year");
            ui.checkbox(&mut self.battery_test, "Process JSON files with new structure");

            if ui.button("Run Script").clicked() {
                self.run_script();
            }
        });
    }
}

impl MyApp {
    fn run_script(&self) {
        let mut args = vec!["d:\\vicky software\\bkp\\bkp\\automation\\server_upload_smb.py"];

        if !self.directory.is_empty() {
            args.push(&self.directory);
        }

        if self.yearly {
            args.push("--yearly");
        }

        if self.battery_test {
            args.push("--battery-test");
        }

        let output = ProcessCommand::new("python3")
            .args(&args)
            .output()
            .expect("Failed to execute Python script");

        if !output.stdout.is_empty() {
            println!("{}", String::from_utf8_lossy(&output.stdout));
        }

        if !output.stderr.is_empty() {
            eprintln!("{}", String::from_utf8_lossy(&output.stderr));
        }
    }
}
