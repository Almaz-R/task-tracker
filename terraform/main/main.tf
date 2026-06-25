# terraform/main/main.tf
resource "yandex_compute_instance" "vm" {
  name        = "task-tracker-master"
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
    subnet_id = "e2l1eklokfgdh7ru5r24"
    nat       = true
  }

  metadata = {
    ssh-keys           = "ubuntu:ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGkPmTnIvpn0EvhRdJAoJyfsHDeSX0AQ9Grz8vVgCoyS"
    serial-port-enable = "1"
  }
}