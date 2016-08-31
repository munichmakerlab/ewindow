#!/bin/sh -ex

mkdir -p build
cd build


build_usrsctp() {
  # Build libusrsctp library
  git clone https://github.com/sctplab/usrsctp
  cd usrsctp
  sh bootstrap
  ./configure --prefix=/opt/janus/
  make
  sudo make install
  cd ..
}


build_janus() {
  # Build Janus WebRTC Gateway
  #git clone https://github.com/meetecho/janus-gateway.git
  cd janus-gateway
  ./autogen.sh
  export CFLAGS="-I/opt/janus/include"
  export LDFLAGS="-L/opt/janus/lib"
  ./configure --prefix=/opt/janus --disable-rabbitmq --disable-docs --disable-websockets
  make CFLAGS="$CFLAGS"
  sudo make install
  cd ..
}


#build_usrsctp
#build_janus
cd ..

sudo cp config/*.cfg /opt/janus/etc/janus/
tar cJf janus-build-$(date +%d%b%g).tar.xz /opt/janus/

set +x
echo
echo =====================
echo Done building janus-build-*.tar.xz
echo =====================
