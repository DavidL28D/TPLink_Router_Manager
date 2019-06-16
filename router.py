import sys

from io import open
from router_handlers.wr340g import TPLinkWR340G

if len(sys.argv) == 1:
    print("Ingrese -h ó --help para solicitar ayuda")

elif len(sys.argv) > 1 and len(sys.argv) <= 3:

    if len(sys.argv) == 2 and (sys.argv[1] == '-h' or sys.argv[1] == "--help"):
        print("Manejo de TPLink.\n\n$ pyhon router.py [Opcion] [Sub-Opcion]\n(Alias)$ router [Opcion] [Sub-Opcion]\n")
        print(" Opciones\tSub-Opcion\tFuncion")
        print("  status\t\t\tMuestra el estado Global del router.")
        print("  ip\t\t\t\tRetorna la IP publica.")
        print("\t\tnew\t\tSolicita renovacion de IP publica.\n")
        print("  mac\t\t\t\tRetorna la MAC.")
        print("\t\tnew\t\tSolicita el cambio de la MAC del router.")
        print("\t\trestart\t\tRestaura la MAC de fabrica.\n")
        print("  ipmac\t\t\t\tSolicita el cambio de la MAC y la IP publica.\n")
        print("  firewall\t\t\tMuestra el estado del Firewall.")
        print("\t\ton\t\tEnciende el Firewall.")
        print("\t\toff\t\tDetiene el Firewall.\n")
        print("  -h, --help\t\t\tImprime esta informacion.\n")
    
    else:

        # credentials.txt
        # username
        # password
        # IP_address

        a = open('credentials.txt', 'r')
        credentials = a.readlines()
        for i in range(2):
            credentials[i] = credentials[i].replace('\n','')

        w = TPLinkWR340G(username=credentials[0], password=credentials[1], ip=credentials[2])
        #w = TPLinkWR340G()

        if sys.argv[1] == "status":
            w.get_status()
            w.get_firewall_status()

        elif sys.argv[1] == "ip":

            if len(sys.argv) == 2:
                print(f"IP publica: {w.get_public_ip()}")
            else:
                if sys.argv[2] == 'new':
                    w.renew_public_ip()
                else:
                    print("Combinacion incorrecta, por favor use -h ó --help si necesita ayuda.")

        elif sys.argv[1] == "mac":

            if len(sys.argv) == 2:
                print(f"MAC del router: {w.get_mac_address()}")
            else:
                if sys.argv[2] == 'new':
                    w.renew_mac_address()
                elif sys.argv[2] == 'restart':
                    w.restart_mac_address()
                else:
                    print("Combinacion incorrecta, por favor use -h ó --help si necesita ayuda.")

        elif len(sys.argv) == 2 and sys.argv[1] == "ipmac":

            w.renew_public_ip_and_mac()

        elif sys.argv[1] == "firewall":

            if len(sys.argv) == 2:
                w.get_firewall_status()
            else:
                if sys.argv[2] == 'on':
                    w.send_firewall_up_request()
                elif sys.argv[2] == 'off':
                    w.send_firewall_down_request()
                else:
                    print("Combinacion incorrecta, por favor use -h ó --help si necesita ayuda.")
        else:
            print("Parametro(s) incorrecto(s), por favor use -h ó --help si necesita ayuda.")

else:
    print("Cantidad de parametros incorrectos, vuelva a intentarlo.")
