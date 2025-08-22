import pywhatkit as pw
txt=""" "I am a passionate developer exploring web technologies,
 AI, and data science.
   I’m currently building a Sunday School Church Portal with engaging designs and admin features.
     I enjoy combining creativity with problem-solving through coding, UI design, and hands-on learning."  """
pw.text_to_handwriting(txt, "sample.png", rgb=[0,0,138])
print("Done")