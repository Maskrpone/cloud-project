{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
	buildInputs = with pkgs; [
		(python3.withPackages(ps: with ps; [
													python-lsp-server
													streamlit
													plotly
		]))
			pyright
			ruff
	];

	shellHook = ''
		echo "Environment up !"
		exec zsh
		'';
}
