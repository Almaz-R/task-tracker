# Используем данные существующей ВМ, не пытаясь создавать новую сеть/подсеть
resource "yandex_compute_instance" "vm_from_terraform" {
  name        = "compute-vm-4-16-50-ssd-1779532794239" # Имя как в облаке
  platform_id = "standard-v4a"
  zone        = "ru-central1-b"

  resources {
    cores  = 4
    memory = 16
  }

  boot_disk {
    initialize_params {
      image_id = "fd8jqd7hb16epiac8lla"
      type     = "network-ssd"
      size     = 50
    }
  }

  network_interface {
    # Вставь сюда ID своей подсети (e2l...)
    subnet_id = "e2l1eklokfgdh7ru5r24"
    nat       = true
  }

  # Метаданные (оставляем пустыми, чтобы не конфликтовать)
  metadata = {
    ssh-keys = "ubuntu:ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGkPmTnIvpn0EvhRdJAoJyfsHDeSX0AQ9Grz8vVgCoyS"
  }
}