import os

def tampilkan_logo():
    RED = "\033[91m"       
    GREEN_TEXT = "\033[92m" 
    RESET = "\033[0m"
    logo_simple = f"""
{GREEN_TEXT}========================================={RESET}                        
{GREEN_TEXT}               {GREEN_TEXT}    /\{RESET}                               
{GREEN_TEXT}               {RED}   /^^\{RESET}                                     
{GREEN_TEXT}               {GREEN_TEXT}  /^^^^\{RESET}                             
{GREEN_TEXT}               {RED} /^^^^^^\{RESET}                                   
{GREEN_TEXT}               {GREEN_TEXT}/^^^^^^^^\{RESET}                           
{GREEN_TEXT}              {RED}/{GREEN_TEXT}__________{RED}\{RESET}                
{GREEN_TEXT}             {RED}/_____{RED}__{RED}_____\{RESET}                      
{GREEN_TEXT}            /______________\ {RESET}                                   
{GREEN_TEXT}       {RED} /______________________\{RESET}                         
{GREEN_TEXT}        |  {GREEN_TEXT}RUMAH MAKAN PADANG {GREEN_TEXT} |{RESET}      
{GREEN_TEXT}        |       {RED}PAPA UDA{GREEN_TEXT}       |{RESET}               
{GREEN_TEXT}        |______________________|{RESET}
{GREEN_TEXT}{RED}/---------------------------------------\{RESET}
{GREEN_TEXT}========================================={RESET}
{GREEN_TEXT}============= Selamat Datang ============{RESET}
{GREEN_TEXT}====== RUMAH MAKAN PADANG PAPA UDA ======{RESET}\n
    """
    print(logo_simple)

#Data Menu
menu_makanan = {
    1: ("Rendang", 13000),
    2: ("Ayam Pop", 12000),
    3: ("Gulai Ayam", 14000),
    4: ("Ikan Bakar", 25000),
    5: ("Sate Padang", 35000),
    6: ("Telur Balado", 7000),
    7: ("Nasi", 3000)
}
menu_minuman = {
    8: ("Teh Manis (Hangat/Dingin) ", 5000),
    9: ("Air Putih (Hangat/Dingin) ", 2000),
    10: ("Es Jeruk", 5000),
    11: ("Es Teler", 8000),
    12: ("Teajus Gulea Bathu", 3000)
}

# menyatukan menu makan dan minum
semua_menu = {}
semua_menu.update(menu_makanan)
semua_menu.update(menu_minuman)

def tampilkan_semua_menu(makanan, minuman):
    LEBAR_NAMA_MAKANAN = 25
    LEBAR_NAMA_MINUMAN = 25 

    print("\n========== | MENU MAKANAN | =============")
    for nomor, (nama, harga) in makanan.items():
        harga_str = f"Rp{harga:,.0f}".replace(",", ".")
        print(f"{nomor}. {nama:<{LEBAR_NAMA_MAKANAN}} {harga_str}")
    print("=========================================")

    print("\n========== | MENU MINUMAN | =============")
    for nomor, (nama, harga) in minuman.items():
        harga_str = f"Rp{harga:,.0f}".replace(",", ".")
        print(f"{nomor}. {nama:<{LEBAR_NAMA_MINUMAN}} {harga_str}")
    print("=========================================\n")


# Program Utama
def main():
    os.system("cls" if os.name == "nt" else "clear")
    tampilkan_logo()

    total = 0
    pesanan = []

    while True:
        tampilkan_semua_menu(menu_makanan, menu_minuman)
        
        try:
            pilihan = int(input("Masukkan nomor menu yang ingin dibeli (0 untuk selesai): "))
        except ValueError:
            print("Input tidak valid! Masukkan angka.")
            continue

        if pilihan == 0:
            break
        elif pilihan in semua_menu:
            nama, harga = semua_menu[pilihan] 
            try:
                jumlah = int(input(f"Masukkan jumlah {nama}: "))
            except ValueError:
                print("Jumlah harus angka!")
                continue

            subtotal = harga * jumlah
            total += subtotal
            pesanan.append((nama, jumlah, subtotal))
            
            subtotal_str = f"Rp{subtotal:,.0f}".replace(",", ".")
            print(f"\n✔ {jumlah} porsi {nama} ditambahkan. Subtotal: {subtotal_str}\n")
        else:
            print("Nomor menu tidak ditemukan! Coba lagi.\n")

    # Output Struk Pembelian
    print("\n================== STRUK PEMBELIAN ===================")
    if not pesanan:
        print("                 Tidak ada pesanan.                   ")
    else:
        for nama, jumlah, subtotal in pesanan:
            subtotal_str = f"Rp{subtotal:,.0f}".replace(",", ".")
            print(f"{nama:<20} ({jumlah}x) = {subtotal_str:>15}") 
    
    total_str = f"Rp{total:,.0f}".replace(",", ".")
    print("======================================================")
    print(f"Total Bayar: {total_str:>40}")
    print("======================================================")
    print("Terima kasih telah berkunjung ke resto kamis")


if __name__ == "__main__":
    main()