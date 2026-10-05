import streamlit as st
import os

st.write("### Dosyalar:")
for f in os.listdir("."):
    path = os.path.join(".", f)
    if os.path.isfile(path):
        size = os.path.getsize(path)
        st.write(f"- {f} : {size} bytes ({size/1024/1024:.2f} MB)")
        if f.endswith(".glb"):
            with open(path, "rb") as file:
                first = file.read(200)
                st.code(first[:200])

st.write("---")
if os.path.exists("motor-v2.glb"):
    s = os.path.getsize("motor-v2.glb")
    if s < 1000:
        st.error(f"motor-v2.glb {s} bytes - Bu LFS pointer! Gerçek dosya değil. Git LFS kurulu değil Cloud'da.")
        st.info("Çözüm: motor-v2.glb'yi https://gltf.report/ ile 10MB altına düşürüp tekrar yükle")
    else:
        st.success(f"motor-v2.glb OK {s/1024/1024:.2f} MB - kod çalışmalı")
