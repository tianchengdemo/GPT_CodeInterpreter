from cli_script import run_chainlit, config

if __name__ == "__main__":
    config.run.headless = False  #根据需要更改
    config.run.debug = False  #根据需要更改
    config.run.no_cache = False  #根据需要更改
    config.run.ci = False  #根据需要更改
    config.run.watch = False  #根据需要更改

    # if 'host':  #如果需要，添加主机
    #   os.environ["CHAINLIT_HOST"] = 'host'
    # if 'port':  #如果需要，添加端口
    #   os.environ["CHAINLIT_PORT"] = 'port'

    run_chainlit('app.py')  # 在这里替换为你实际想运行的文件名或路径
