import os
import getpass
import sys


# 1.DATABASE
akun_db = {
    "admin1": {"password": "123", "role": "admin"},
    "user1": {"password": "123", "role": "user"}
}

# Format: ID: [Nama, Harga, Stok]
menu_rm = {
    1: ["Rendang", 13000, 10],
    2: ["Ayam Pop", 12000, 15],
    3: ["Gulai Ayam", 14000, 8],
    4: ["Ikan Bakar", 25000, 5],
    5: ["Sate Padang", 35000, 12],
    6: ["Telur Balado", 7000, 20],
    7: ["Nasi Putih", 3000, 50],
    8: ["Teh Manis", 5000, 30],
    9: ["Es Jeruk", 5000, 15]
}


#FUNGSI UTILITY (Pembantu)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def garis():
    print("=" * 50)

def format_rupiah(angka):
    return f"Rp{angka:,.0f}".replace(",", ".")

def tampilkan_tabel_menu():
    garis()
    print(f"{'ID':<4} | {'Nama Menu':<20} | {'Harga':<12} | {'Stok'}")
    garis()
    for id_m, data in menu_rm.items():
        stok = "HABIS" if data[2] <= 0 else data[2]
        print(f"{id_m:<4} | {data[0]:<20} | {format_rupiah(data[1]):<12} | {stok}")
    garis()


# 3. FITUR ADMIN
def menu_admin(nama):
    while True:
        clear()
        print(f"DASHBOARD ADMIN: {nama.upper()}")
        print("[1] Lihat & Tambah Stok")
        print("[2] Tambah Produk Baru")
        print("[0] Logout")
        
        pilih = input("\nPilih Menu > ")
        
        if pilih == "1":
            tampilkan_tabel_menu()
            try:
                id_m = int(input("Masukkan ID Menu untuk restok: "))
                if id_m in menu_rm:
                    tambah = int(input(f"Jumlah stok tambahan untuk {menu_rm[id_m][0]}: "))
                    menu_rm[id_m][2] += tambah
                    print("✔ Stok berhasil diperbarui!")
                else:
                    print("ID tidak ditemukan.")
            except ValueError:
                print("Masukkan angka yang valid!")
            input("\nTekan Enter...")
            
        elif pilih == "2":
            try:
                id_baru = max(menu_rm.keys()) + 1
                nama_p = input("Nama Produk Baru: ")
                harga_p = int(input("Harga: "))
                stok_p = int(input("Stok Awal: "))
                menu_rm[id_baru] = [nama_p, harga_p, stok_p]
                print(f"✔ {nama_p} berhasil ditambahkan ke menu!")
            except ValueError:
                print("Gagal. Pastikan harga dan stok berupa angka.")
            input("\nTekan Enter...")
            
        elif pilih == "0":
            break


# 4. FITUR USER
def menu_user(nama):
    keranjang = []
    total_bayar = 0
    
    while True:
        clear()
        print(f"HALO {nama.upper()}, SELAMAT DATANG DI RM PADSKUY!")
        tampilkan_tabel_menu()
        print("(Ketik '0' untuk selesai dan cetak struk)")
        
        try:
            pilih = int(input("Pilih ID Menu > "))
            if pilih == 0: break
            
            if pilih in menu_rm:
                if menu_rm[pilih][2] <= 0:
                    print(f"Maaf, {menu_rm[pilih][0]} sedang habis!")
                else:
                    qty = int(input(f"Beli berapa {menu_rm[pilih][0]}? "))
                    if qty > menu_rm[pilih][2]:
                        print(f"Stok tidak cukup! (Sisa: {menu_rm[pilih][2]})")
                    elif qty <= 0:
                        print("Pembelian minimal 1.")
                    else:
                        # PENGURANGAN STOK OTOMATIS
                        menu_rm[pilih][2] -= qty
                        subtotal = menu_rm[pilih][1] * qty
                        total_bayar += subtotal
                        keranjang.append([menu_rm[pilih][0], qty, subtotal])
                        print(f"✔ Berhasil menambah {qty} {menu_rm[pilih][0]}")
            else:
                print("Menu tidak tersedia.")
        except ValueError:
            print("Masukkan angka!")
        input("\nTekan Enter...")

    if keranjang:
        clear()
        print("\n" + " " * 12 + "STRUK PEMBELIAN RM PADSKUY")
        garis()
        for item in keranjang:
            print(f"{item[0]:<20} x{item[1]:<3} | {format_rupiah(item[2]):>15}")
        garis()
        print(f"{'TOTAL BAYAR':<25} | {format_rupiah(total_bayar):>15}")
        garis()
        print("   Terima kasih sudah memesan di RM PADSKUY!   ")
        input("\nTekan Enter untuk logout...")


# 5. AUTHENTICATION & MAIN FLOW
def main():
    while True:
        clear()
        garis()
        print(f"{'LOGIN SISTEM RM PADSKUY':^50}")
        garis()
        user = input("Username: ")
        
        if user in akun_db:
            pw = getpass.getpass("Password: ")
            if akun_db[user]["password"] == pw:
                # Cek Role
                if akun_db[user]["role"] == "admin":
                    menu_admin(user)
                else:
                    menu_user(user)
            else:
                print("\n[!] Password salah!")
                input("Enter...")
        else:
            print("\n[!] Akun tidak terdaftar!")
            input("Enter...")

if __name__ == "__main__":
    main()