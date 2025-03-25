# log_upload_script_plus_misc

Anticimex scripts that I wrote and what could have been if more time was given to me

## Build Instructions

1. **Install Rust and Cargo**:
   Follow the instructions at [rustup.rs](https://rustup.rs/) to install Rust and Cargo.

2. **Install Dependencies**:
   Navigate to the project directory and run:
   ```sh
   cargo build
   ```

3. **Build the Application**:
   Run the following command to build the application:
   ```sh
   cargo build --release
   ```

4. **Run the Application**:
   Execute the built application:
   ```sh
   ./target/release/rust_frontend
   ```

5. **Run the Python Script**:
   Ensure you have Python installed and run the Python script as needed:
   ```sh
   python3 d:\\vicky software\\bkp\\bkp\\automation\\server_upload_smb.py
   ```

## Cross-Platform Build Instructions

### Prerequisites
1. Install Rust and Cargo from [rust-lang.org](https://www.rust-lang.org/).
2. Install the required Rust toolchains for cross-compilation:
   ```sh
   rustup target add x86_64-unknown-linux-gnu
   rustup target add x86_64-apple-darwin
   ```

3. For Linux builds:
   - On Windows, install a cross-compilation tool like `mingw-w64` or `gcc` for Linux.
   - On macOS, you can use `brew install gcc`.

4. For macOS builds:
   - On Windows, you need a macOS cross-compiler like `osxcross`.
   - On Linux, you can use `osxcross` or `clang`.

### Building Executables
Run the following commands to build the application for different platforms:

#### For Windows
```sh
cargo build --release
```
The executable will be located in `target/release/rust_frontend.exe`.

#### For Linux
```sh
cargo build --release --target x86_64-unknown-linux-gnu
```
The executable will be located in `target/x86_64-unknown-linux-gnu/release/rust_frontend`.

#### For macOS
```sh
cargo build --release --target x86_64-apple-darwin
```
The executable will be located in `target/x86_64-apple-darwin/release/rust_frontend`.

### Running the Application
After building the application, run the executable on the respective platform:
- **Windows**: Double-click the `.exe` file or run it from the command line.
- **Linux/macOS**: Run the executable from the terminal:
  ```sh
  ./rust_frontend
  ```

### Notes
- Ensure that the Python script (`server_upload_smb.py`) is accessible and properly configured.
- For macOS, you may need to sign the executable or allow it to run in your system preferences.
