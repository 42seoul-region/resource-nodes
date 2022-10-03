# 자원 노드 설치 스크립트

## 1. 공통 설치
### (1) 네트워크 및 관리 도구 설치
```bash
./install-network.sh
```

## 2. 컴퓨트(Compute) 노드
### (1) VLAN 설정
```bash
$ ./vlan.sh 192.168.42.2/24 192.168.42.255
```
현재 노드의 IP/CIDR, 브로드캐스트 주소를 인자로 넣음.
### (2) 환경 변수 수정
```
HOST_VLAN_CONTROLLER=192.168.42.1
HOST_PUBLIC_CONTROLLER=10.211.55.7
```
`compute-node/.env` 파일에서 컨트롤러의 VLAN주소 및 공개 주소를 수정.
### (3) 설치 스크립트 실행
```bash
$ ./compute-node/startup.sh
```

## 3. 끝
