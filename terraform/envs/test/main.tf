resource "yandex_compute_instance" "vm" {
  name        = "task-tracker-vm-${var.environment}"
  platform_id = "standard-v4a"
  zone        = "ru-central1-b"

  resources {
    cores  = var.environment == "prod" ? 8 : 4
    memory = var.environment == "prod" ? 32 : 16
  }

  boot_disk {
    initialize_params {
      image_id = "fd8jqd7hb16epiac8lla"
      type     = "network-ssd"
      size     = var.environment == "prod" ? 100 : 50
    }
  }

  network_interface {
    subnet_id = "e2l1eklokfgdh7ru5r24"
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGkPmTnIvpn0EvhRdJAoJyfsHDeSX0AQ9Grz8vVgCoyS"
  }
}