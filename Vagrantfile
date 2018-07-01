Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"

  config.vm.provision "shell", path: "provision.sh"
  config.vm.network "forwarded_port", guest: 80, host: 5000

  config.vm.synced_folder ".", "/simple_login",
      type: "rsync",
      owner: "vagrant",
      rsync__exclude: ["env/", "flask_session/", ".git/", ".gitignore", ".mypy_cache", ".vagrant/"]
end
