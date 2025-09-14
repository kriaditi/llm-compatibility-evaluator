import subprocess

# Full absolute path to ollama.exe
ollama_path = r"C:\Users\Aditi\AppData\Local\Programs\Ollama\ollama.exe"

def call_mistral(prompt: str) -> str:
    """Call Ollama with full path using subprocess."""
    try:
        process = subprocess.Popen(
            [ollama_path, 'run', 'mistral'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate(input=prompt.encode(), timeout=300)

        if process.returncode != 0:
            print(" Ollama subprocess error:", stderr.decode())
            return " mistral model failed to respond."

        return stdout.decode()

    except subprocess.TimeoutExpired:
        process.kill()
        return " Timeout: mistral model took too long."

    except Exception as e:
        return f" Unexpected error: {e}"