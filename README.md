LaTeXDS
--
This is user-installable Discord application that adds command for rendering LaTeX.

![Example usage](../assets/example.png?raw=true)

----------

# Install already existing instance
[Click there](https://latexds.nakidai.ru)

# Run your own instance
Since this bot is open source you can selfhost it. I would say that this way is preferable since I use slow host.
## Without docker
- Set either `LATEXDS_TOKEN` to token of your bot or `LATEXDS_TOKEN_FILE` to path to file with token  
- Run `latexds`  
## With docker
- Create secret named `latexds-token` with your token  
- Download `nakidai/latexds:latest`  
- Run `docker stack deploy -c compose.yml latexds`  
