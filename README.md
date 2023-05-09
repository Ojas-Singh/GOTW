# GOTW Automation

```
conda create --name AmberTools23
conda activate AmberTools23
pip install streamlit biopython requests
sudo iptables -t nat -I OUTPUT -p tcp -d 127.0.0.1 --dport 8080 -j REDIRECT --to-ports 3001
sudo iptables -t nat -I PREROUTING -p tcp --dport 8080 -j REDIRECT --to-ports 3001
streamlit run website

```
