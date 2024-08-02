from amocrm.v2 import tokens, Lead, Pipeline


if __name__ == '__main__':
    tokens.default_token_manager(
        client_id="8ed85464-b8f9-4be8-b90b-da960d365bcf",
        client_secret="XAEUkjDTtzYCSE8aPeKfnbCdH2HigFPEw6EsMifNZmTznaXBrT3dGB6HEoxm5g5M",
        subdomain="mkrgkz",
        redirect_url="https://yandex.kz/",
        storage=tokens.FileTokensStorage(),  # by default FileTokensStorage
    )
    # tokens.default_token_manager.init(code="def502001d5a0000c4bfc8dd547e696305b18a75bfaa3026f096342100731137858ec173e614d1a5ebeb9e515d16b39ec494c9f855e82681b5d34613c978274014f40ad1b82d69d4defeee9a4c9ea42c01468832e372272bdab49ea5fc5a33b11a4ea106e8c669f58c21754aebd9e69d235949203a5f5cefdfe35425ebafe3b717420cbfb4fffbf970b8e56902c240beba066360bdbd0e7a8edda49fd3d073539d21f7d321475d4af42e456e04b2c35104cd4cd6a7a50436339e7f2b0998851b3b2cc641b5adfac07c8af8a8e2485481ad0aef2f793c2ece90e977e9d5385ef48ad9ab05880054696b87ef49404021733cc36363c3dcf154d20e82d745a440441d67b0afa0af0e092b9d54a5732b1c235b88f97f609f71112fb5f03fc12d74ff87ab4804cda111b90ed8c0b44a6e9ac3a15f34d7ba7d1140fdad22029bafdd1914b0059fd23b71606388fe3d28a914d6255f8aa26828b797542a4acf67264894fb6b6c7a66c83408771cf2bdac5ebf14a34c0257bd73bb19caf4399948d8bc130bdc25ad1fcd7413c67cd2bdcb2983d6026d3b95a42db5f27953485a2a758d39b530c131c9180f1627b033414f028e6f3073471db2f3faf72d48b01f5fc4d14ff2ca11e5cde784a66fe085b2803045a6c396228162c5ca0d4fa8c6ff7abf8e2e357900dd",
    #                                 skip_error=False)

    lead = Lead.objects.get(query="первый этап")
    # for lead in leads:
        # print(lead)
    print(lead.name, lead.price, lead.id, lead.contacts)