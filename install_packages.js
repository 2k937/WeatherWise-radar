const { exec } = require("child_process");

function runCommand(command, description) {
    return new Promise((resolve, reject) => {
        console.log(`\n➡️ Running: ${description}`);
        const process = exec(command, (error, stdout, stderr) => {
            if (error) {
                console.error(`❌ Error during ${description}:\n`, error);
                reject(error);
            } else {
                console.log(stdout);
                resolve();
            }
        });
        process.stdout.pipe(process.stdout);
        process.stderr.pipe(process.stderr);
    });
}

async function main() {
    try {
        // 1️⃣ Install Node packages
        await runCommand("npm install", "Installing Node.js packages");

        // 2️⃣ Install Python packages
        await runCommand("pip install -r requirements.txt", "Installing Python packages");

        // 3️⃣ Start Node.js server
        console.log("\n🚀 Starting Node.js server...");
        const server = exec("node server.js");
        server.stdout.pipe(process.stdout);
        server.stderr.pipe(process.stderr);

    } catch (err) {
        console.error("⚠️ Installation failed:", err);
    }
}

main();