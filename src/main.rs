use eframe::{egui, App, NativeOptions};
use native_dialog::FileDialog;
use std::process::Command as ProcessCommand;

fn main() {
    let options = NativeOptions {
        ..Default::default() // Use default options
    };
    let _ = eframe::run_native(
        "Rust Frontend GUI",
        options,
        Box::new(|_cc| Ok(Box::new(MyApp::default()))),
    );
}

struct MyApp {
    directory: String,
    yearly: bool,
    battery_test: bool,
    server_ip: String,
    share_name: String,
    destination_path: String,
    username: String,
    password: String,
}

impl Default for MyApp {
    fn default() -> Self {
        Self {
            directory: String::new(),
            yearly: false,
            battery_test: false,
            server_ip: "172.22.41.14".to_string(),
            share_name: "AIC-Helsinge".to_string(),
            destination_path: "SMART_CATCH_MINI".to_string(),
            username: "aicprod\\AIC-SVC_FileExport".to_string(),
            password: "Ju$5LKEbreU!".to_string(),
        }
    }
}

impl App for MyApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::CentralPanel::default().show(ctx, |ui| {
            ui.vertical_centered(|ui| {
                ui.heading("Rust Frontend for Python SMB Upload Script");
            });

            ui.separator();

            ui.vertical_centered(|ui| {
                ui.heading("Configuration Settings:");
                ui.vertical_centered(|ui| {
                    ui.horizontal(|ui| {
                        ui.label("Server IP:");
                        ui.text_edit_singleline(&mut self.server_ip);
                    });
                    ui.horizontal(|ui| {
                        ui.label("Share Name:");
                        ui.text_edit_singleline(&mut self.share_name);
                    });
                    ui.horizontal(|ui| {
                        ui.label("Destination Path:");
                        ui.text_edit_singleline(&mut self.destination_path);
                    });
                    ui.horizontal(|ui| {
                        ui.label("Username:");
                        ui.text_edit_singleline(&mut self.username);
                    });
                    ui.horizontal(|ui| {
                        ui.label("Password:");
                        ui.text_edit_singleline(&mut self.password);
                    });
                });
            });

            ui.separator();

            ui.vertical_centered(|ui| {
                if ui.button("Select Directory").clicked() {
                    if let Some(path) = FileDialog::new().show_open_single_dir().ok().flatten() {
                        self.directory = path.to_string_lossy().to_string();
                    }
                }

                ui.label(format!("Selected Directory: {}", self.directory));

                ui.checkbox(&mut self.yearly, "Aggregate data by year");
                ui.checkbox(&mut self.battery_test, "Process JSON files for battery test");

                if ui.button("Run Script").clicked() {
                    self.run_script();
                }
            });
        });

        // Dynamically adjust the UI by repainting
        ctx.request_repaint();
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

        args.push("--server-ip");
        args.push(&self.server_ip);
        args.push("--share-name");
        args.push(&self.share_name);
        args.push("--destination-path");
        args.push(&self.destination_path);
        args.push("--username");
        args.push(&self.username);
        args.push("--password");
        args.push(&self.password);

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
