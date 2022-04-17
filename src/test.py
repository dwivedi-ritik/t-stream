def parse_config():
    app_dir = "/".join(os.path.realpath(__file__).split("/")[:-2])
    config_path = os.path.join(app_dir , "config.json")

    default_value = ("webtorrent" , "mpv")
    players = ["mpv" , "vlc"]
    clients = ["webtorrent" , "peerflix"]

    if not Path(config_path).is_file():
        return default_value

    with open(config_path) as f:
        config = json.loads(f.read())
    
    if config["config"]["player"] and config["config"]["client"]:
        if config["config"]["player"] in players and config["config"]["client"] in clients:
            return ( config["config"]["player"] , config["config"]["client"] )
    
    return default_value
        
