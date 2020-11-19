from vkApi import VkApi

client_id = 7669046
client_secret = "f7K07lCcfsYhyk3X5Py1"

ans = VkApi.get_access_token(client_id, client_secret)
print(ans)

exit(0)
