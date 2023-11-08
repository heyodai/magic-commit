// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');
const { exec } = require('child_process');

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
	let disposable = vscode.commands.registerCommand('extension.magicCommit', () => {
		// Assuming magic-commit is in the system PATH
		exec('magic-commit --no-load', (error, stdout, stderr) => {
		  if (error) {
			vscode.window.showErrorMessage(`Error: ${stderr}`);
			return;
		  }
		  const gitInputBox = vscode.window.createInputBox();
		  gitInputBox.value = stdout;
		  gitInputBox.placeholder = 'Commit message';
		  gitInputBox.show();
		});
	  });
	
	  context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate
}
