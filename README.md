# TWRP Builder — POCO X6 Pro (duchamp)

Build TWRP recovery untuk POCO X6 Pro (codename **duchamp**, Dimensity 8300 Ultra / mt6897) sepenuhnya lewat GitHub Actions. Tanpa PC.

## Cara build

1. Buka tab **Actions** → workflow **Build TWRP (duchamp)** → **Run workflow**.
2. Semua parameter sudah terisi default duchamp — langsung **Run workflow** tanpa ubah apa-apa.
3. Tunggu: sync source ±15–25 menit, lalu build ±30–60 menit.
4. Hasil build (`boot.img`) muncul di tab **Releases** (tag = nomor run).

## Yang dipakai

- Manifest: `minimal-manifest-twrp/platform_manifest_twrp_aosp`, branch `twrp-12.1` (tidak memuat `vendor/omni` — di-clone terpisah dari `omnirom/android_vendor_omni`, branch `android-12.1`)
- Device tree: `hozin-king/android_device_xiaomi_duchamp` (branch `main`) — fork dari `renton16/android_device_xiaomi_duchamp`, dengan perbaikan: hapus `PRODUCT_STATIC_BOOT_CONTROL_HAL` (obsolete, gagal saat lunch). Perbaikan tree selanjutnya dikumpulkan di fork ini.
- Kernel prebuilt: `mt6897-devs/device_xiaomi_duchamp-kernel` (`Image.lz4` + `dtb/mt6897.dtb`, branch `lineage-23.2`) — tree publik duchamp tidak menyertakan `prebuilt/kernel`, jadi kernel diambil saat build.
- Target: `boot` — duchamp A/B memakai `BOARD_USES_RECOVERY_AS_BOOT=true`, jadi recovery hidup di dalam `boot.img` (bukan partisi recovery dan bukan `vendor_boot`).

## Cara flash (baca sampai habis sebelum flash)

**Syarat:** bootloader sudah unlock.

**Dengan PC (paling aman — tes dulu tanpa flash):**

```
fastboot boot boot.img
```

Kalau TWRP muncul dan sentuhan jalan, baru flash permanen:

```
fastboot flash boot_a boot.img
fastboot flash boot_b boot.img
fastboot reboot recovery
```

**Tanpa PC (hanya via root):** backup dulu boot yang sekarang (isinya KernelSU/root kamu!), lalu flash via Termux sebagai root:

```
su
dd if=/dev/block/by-name/boot_a of=/sdcard/boot_stock.img
```

Perintah flash yang benar (ganti `<file>` dengan boot.img hasil build):

```
dd if=<file> of=/dev/block/by-name/boot_a
dd if=<file> of=/dev/block/by-name/boot_b
```

## ⚠️ PERINGATAN — baca dulu

- **Flash `boot.img` menimpa boot yang sekarang, termasuk root KernelSU kamu.** Setelah flash, root hilang sampai boot di-patch ulang KernelSU. Simpan `boot_stock.img` hasil backup baik-baik.
- **Kalau `boot.img` hasil build gagal boot, HP tidak bisa masuk sistem.** Balikinnya butuh fastboot dari PC (`fastboot flash boot_a boot_stock.img`). Tanpa PC, tidak ada jalan pulih dari kondisi ini.
- **Dekripsi /data kemungkinan TIDAK jalan** di TWRP ini (tidak ada flag crypto di tree; umum di MediaTek + HyperOS). Artinya backup/restore partisi data dari TWRP kemungkinan gagal — TWRP tetap berguna untuk flash ZIP, wipe, dan install custom ROM.
- Build pertama hampir pasti butuh 1–3x iterasi perbaikan (fstab/kernel/dtb). Itu normal.
