from pymemcache import client


class Client(client.Client):
    get_multi = client.Client.get_many
    set_multi = client.Client.set_many
    delete_multi = client.Client.delete_many
    disconnect_all = client.Client.quit
