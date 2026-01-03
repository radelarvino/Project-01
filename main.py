from migrate import migrate
from db import fetch_all, fetch_one, execute
import os
import getpass

# 2. FUNGSI UTILITY
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def garis():
    print("=" * 50)

def format_rupiah(angka):
    return f"Rp{angka:,.0f}".replace(",", ".")

def tampilkan_tabel_menu():
    data_menu = fetch_all("SELECT * FROM menus")

    garis()
    print(f"{'ID':<4} | {'Nama Menu':<20} | {'Harga':<12} | {'Stok'}")
    garis()

    for m in data_menu:
        stock = "HABIS" if m["stock"] <= 0 else m["stock"]
        print(f"{m['id']:<4} | {m['name']:<20} | {format_rupiah(m['price']):<12} | {stock}")

    garis()

def restock_menu(id_menu, quantity):
    execute(
            "UPDATE menus SET stock = stock + ? WHERE id = ?",
            (quantity, id_menu)
            )

def add_menu(name, price, stock):
    execute(
            "INSERT INTO menus (name, price, stock) VALUES (?, ?, ?)",
            (name, price, stock)
            )

def register_user(username, password, role):
    execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, role)
            )

# 3. FITUR ADMIN
def menu_admin(nama_admin):
    while True:
        clear()
        print(f"DASHBOARD ADMIN: {nama_admin.upper()}")
        print("[1] Lihat & Tambah Stok")
        print("[2] Tambah Produk Baru")
        print("[0] Logout")
        
        pilih = input("\nPilih Menu > ")
        
        if pilih == "1":
            tampilkan_tabel_menu()
            try:
                id_m = int(input("Masukkan ID Menu untuk restok: "))
                menu = fetch_one("SELECT * FROM menus WHERE id = ?", (id_m,))

                if menu:
                    quantity = int(input(f"Jumlah stok tambahan: "))

                    restock_menu(id_m, quantity)

                    print("✔ Stok berhasil diperbarui!")
                else:
                    print("ID tidak ditemukan.")
            except ValueError:
                print("Masukkan angka yang valid!")
            input("\nTekan Enter...")
            
        elif pilih == "2":
            try:
                nama_p = input("Nama Produk Baru: ")
                harga_p = int(input("Harga: "))
                stok_p = int(input("Stok Awal: "))

                add_menu(nama_p, harga_p, stok_p)

                print(f"✔ {nama_p} berhasil ditambahkan ke menu!")
            except ValueError:
                print("Gagal. Pastikan harga dan stok berupa angka.")
            input("\nTekan Enter...")
            
        elif pilih == "0":
            break


# 4. FITUR USER
def menu_user(nama_user):
    keranjang = []
    total_bayar = 0
    
    while True:
        clear()
        print(f"HALO {nama_user.upper()}, SELAMAT DATANG DI RM PADSKUY!")
        tampilkan_tabel_menu()
        print("(Ketik '0' untuk selesai dan cetak struk)")
        
        try:
            pilih = int(input("Pilih ID Menu > "))
            if pilih == 0: break
            
            menu = fetch_one(
                    "SELECT * FROM menus WHERE id = ?",
                    (pilih,)
                    )

            if not menu:
                print("Menu tidak tersedia!")
            elif menu["stock"] <= 0:
                print(f"Maaf, {menu['name']} sedang habis!")
            else:
                qty = int(input(f"Beli berapa {menu['name']}? "))

                if qty <= 0:
                    print("Pembelian minimal 1.")
                elif qty > menu["stock"]:
                    print(f"Stok tidak cukup! (Sisa: {menu['stock']})")
                else:
                    execute(
                            "UPDATE menus SET stock = stock - ? WHERE id = ?",
                            (qty, pilih)
                            )

                    subtotal = menu["price"] * qty
                    total_bayar += subtotal

                    keranjang.append([
                        menu["name"],
                        qty,
                        subtotal
                        ])

                    print(f"✔ Berhasil menambah {qty} {menu['name']}")
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
        print(f"{'SELAMAT DATANG DI RM PADSKUY':^50}")
        garis()
        print("[1] Login")
        print("[2] Register")
        print("[0] Keluar Aplikasi")
        opsi = input("Pilih Opsi > ")

        if opsi == "1":
            clear()
            garis()
            print(f"{'MASUK AKUN':^50}")
            garis()
            username = input("Username: ")
            password = getpass.getpass("Password: ")

            account = fetch_one(
                    "SELECT * FROM users WHERE username = ? AND password = ?", 
                    (username, password)
                    )
            
            if account:
                if account["role"] == "admin":
                    menu_admin(account['username'])
                else:
                    menu_user(account['username'])
            else:
                print("\nLogin gagal! Username atau password salah.")
                input("Tekan Enter untuk kembali...")

        elif opsi == "2":
            clear()
            garis()
            print(f"{'DAFTAR AKUN BARU':^50}")
            garis()
            username = input("Username Baru: ")

            user_check = fetch_one("SELECT id FROM users WHERE username = ?", (username,))

            if user_check:
                print("Username sudah terdaftar!")
            else:
                password = input("Password Baru: ")
                role = input("Role (admin/user): ").lower()
                if role in ["admin", "user"]:
                    register_user(username, password, role)

                    print(f"✔ Registrasi berhasil sebagai {role.upper()}!")
                else:
                    print("Role tidak valid!")
            input("Tekan Enter untuk kembali...")

        elif opsi == "0":
            print("sampai jumpo!")
            break

if __name__ == "__main__":
    migrate()
    main()
