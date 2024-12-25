from tkinter import *
import tkinter.filedialog
from PIL import ImageTk, Image
from tkinter import messagebox
from io import BytesIO
import os
from encrypt import encryptMessage, decryptMessage

class ModernStegno:
    def __init__(self):
        # UI Colors
        self.primary_color = "#2196F3"
        self.secondary_color = "#FFC107"
        self.bg_color = "#F5F5F5"
        self.text_color = "#212121"
        
        # Fonts
        self.title_font = ('Helvetica', 24, 'bold')
        self.button_font = ('Helvetica', 12)
        self.text_font = ('Helvetica', 11)
        
        # Image properties
        self.output_image_size = 0
        self.o_image_w = 0
        self.o_image_h = 0
        self.d_image_w = 0
        self.d_image_h = 0
        self.d_image_size = 0

    def main(self, root):
        root.title('Image Steganography')
        root.geometry('900x700')
        root.configure(bg=self.bg_color)
        
        main_frame = Frame(root, bg=self.bg_color, padx=20, pady=20)
        
        # Title Section
        title = Label(main_frame, 
                     text='Image Steganography',
                     font=self.title_font,
                     bg=self.bg_color,
                     fg=self.text_color)
        title.pack(pady=(0, 20))
        
        # Buttons
        encode_btn = Button(main_frame, 
                          text="Encode Message",
                          command=lambda: self.frame1_encode(main_frame),
                          bg=self.primary_color,
                          fg='white',
                          font=self.button_font,
                          padx=20,
                          pady=10,
                          relief='flat',
                          cursor='hand2')
        encode_btn.pack(pady=10, padx=100, fill=X)
        
        decode_btn = Button(main_frame,
                          text="Decode Message",
                          command=lambda: self.frame1_decode(main_frame),
                          bg=self.primary_color,
                          fg='white',
                          font=self.button_font,
                          padx=20,
                          pady=10,
                          relief='flat',
                          cursor='hand2')
        decode_btn.pack(pady=10, padx=100, fill=X)
        
        # Credits
        credits = Label(main_frame,
                       text="\nCreated by:\nTanush (22103157)\nSaumil Gupta (22103179)\nKaran Naveen Sood (22103180)",
                       font=('Helvetica', 10),
                       bg=self.bg_color,
                       fg='#666666')
        credits.pack(pady=20)
        
        main_frame.pack(expand=True, fill='both')

    def frame1_decode(self, f):
        f.destroy()
        decode_frame = Frame(root, bg=self.bg_color, padx=20, pady=20)
        
        # Title
        Label(decode_frame,
              text="Decode Hidden Message",
              font=self.title_font,
              bg=self.bg_color,
              fg=self.text_color).pack(pady=20)
        
        # Key Input
        key_frame = Frame(decode_frame, bg=self.bg_color)
        Label(key_frame,
              text="Enter Decryption Key:",
              font=self.text_font,
              bg=self.bg_color).pack(side=LEFT, padx=5)
        text_area = Text(key_frame, width=20, height=1, font=self.text_font)
        text_area.pack(side=LEFT, padx=5)
        key_frame.pack(pady=20)
        
        # Image Selection
        Label(decode_frame,
              text="Select Image with Hidden Message:",
              font=self.text_font,
              bg=self.bg_color).pack(pady=10)
        
        select_btn = Button(decode_frame,
                          text="Choose Image",
                          command=lambda: self.frame2_decode(decode_frame, text_area),
                          bg=self.primary_color,
                          fg='white',
                          font=self.button_font,
                          relief='flat',
                          cursor='hand2')
        select_btn.pack(pady=10)
        
        # Back Button
        Button(decode_frame,
               text="Back",
               command=lambda: self.home(decode_frame),
               bg='#9E9E9E',
               fg='white',
               font=self.button_font,
               relief='flat',
               cursor='hand2').pack(pady=20)
        
        decode_frame.pack(expand=True, fill='both')

    def frame2_decode(self, d_f2, text_area):
        key = text_area.get("1.0", "end-1c")
        if not key:
            messagebox.showerror("Error", "Please enter a decryption key!")
            return
            
        myfile = tkinter.filedialog.askopenfilename(filetypes=(
            ('PNG files', '*.png'), ('All Files', '*.*')))
            
        if not myfile:
            messagebox.showerror("Error", "No image selected!")
            return
            
        try:
            myimg = Image.open(myfile, 'r')
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            
            d_f3 = Frame(root, bg=self.bg_color, padx=20, pady=20)
            
            Label(d_f3,
                  text="Selected Image:",
                  font=self.text_font,
                  bg=self.bg_color).pack(pady=10)
                  
            panel = Label(d_f3, image=img)
            panel.image = img
            panel.pack()
            
            # Get hidden data
            try:
                hidden_data = self.decode(myimg, key)
                Label(d_f3,
                      text="Hidden Message:",
                      font=self.text_font,
                      bg=self.bg_color).pack(pady=10)
                      
                text_area = Text(d_f3, width=50, height=10, font=self.text_font)
                text_area.insert(INSERT, hidden_data)
                text_area.configure(state='disabled')
                text_area.pack(pady=10)
                
            except Exception as e:
                messagebox.showerror("Error", "Failed to decode message. Check your encryption key.")
                return
            
            Button(d_f3,
                   text="Back to Main",
                   command=lambda: self.home(d_f3),
                   bg=self.primary_color,
                   fg='white',
                   font=self.button_font,
                   relief='flat',
                   cursor='hand2').pack(pady=20)
                   
            d_f3.pack(expand=True, fill='both')
            d_f2.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", "Failed to open image!")

    def frame1_encode(self, f):
        f.destroy()
        encode_frame = Frame(root, bg=self.bg_color, padx=20, pady=20)
        
        Label(encode_frame,
              text="Encode Secret Message",
              font=self.title_font,
              bg=self.bg_color,
              fg=self.text_color).pack(pady=20)
              
        Label(encode_frame,
              text="Select an Image:",
              font=self.text_font,
              bg=self.bg_color).pack(pady=10)
              
        Button(encode_frame,
               text="Choose Image",
               command=lambda: self.frame2_encode(encode_frame),
               bg=self.primary_color,
               fg='white',
               font=self.button_font,
               relief='flat',
               cursor='hand2').pack(pady=10)
               
        Button(encode_frame,
               text="Back",
               command=lambda: self.home(encode_frame),
               bg='#9E9E9E',
               fg='white',
               font=self.button_font,
               relief='flat',
               cursor='hand2').pack(pady=20)
               
        encode_frame.pack(expand=True, fill='both')

    def frame2_encode(self, f2):
        ep = Frame(root, bg=self.bg_color, padx=20, pady=20)
        
        myfile = tkinter.filedialog.askopenfilename(filetypes=(
            ('PNG files', '*.png'), ('All Files', '*.*')))
            
        if not myfile:
            messagebox.showerror("Error", "No image selected!")
            return
            
        try:
            myimg = Image.open(myfile)
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            
            Label(ep,
                  text="Selected Image:",
                  font=self.text_font,
                  bg=self.bg_color).pack(pady=10)
                  
            panel = Label(ep, image=img)
            panel.image = img
            panel.pack()
            
            self.output_image_size = os.stat(myfile)
            self.o_image_w, self.o_image_h = myimg.size
            
            # Message Entry
            Label(ep,
                  text="Enter Your Message:",
                  font=self.text_font,
                  bg=self.bg_color).pack(pady=10)
            text_area = Text(ep, width=50, height=10, font=self.text_font)
            text_area.pack(pady=10)
            
            # Key Entry
            Label(ep,
                  text="Enter Encryption Key:",
                  font=self.text_font,
                  bg=self.bg_color).pack(pady=10)
            key_area = Text(ep, width=20, height=1, font=self.text_font)
            key_area.pack(pady=10)
            
            # Buttons
            Button(ep,
                   text="Encode",
                   command=lambda: self.enc_fun(text_area, myimg, key_area),
                   bg=self.primary_color,
                   fg='white',
                   font=self.button_font,
                   relief='flat',
                   cursor='hand2').pack(pady=10)
                   
            Button(ep,
                   text="Back",
                   command=lambda: self.home(ep),
                   bg='#9E9E9E',
                   fg='white',
                   font=self.button_font,
                   relief='flat',
                   cursor='hand2').pack(pady=10)
                   
            ep.pack(expand=True, fill='both')
            f2.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", "Failed to open image!")

    def decode(self, image, key):
        data = ''
        imgdata = iter(image.getdata())
        
        while True:
            pixels = [value for value in imgdata.__next__()[:3] +
                      imgdata.__next__()[:3] +
                      imgdata.__next__()[:3]]
            
            binstr = ''
            for i in pixels[:8]:
                if i % 2 == 0:
                    binstr += '0'
                else:
                    binstr += '1'
            
            data += chr(int(binstr, 2))
            if pixels[-1] % 2 != 0:
                return decryptMessage(data, key)

    def genData(self, data):
        newd = []
        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

    def modPix(self, pix, data):
        datalist = self.genData(data)
        lendata = len(datalist)
        imdata = iter(pix)
        
        for i in range(lendata):
            pix = [value for value in imdata.__next__()[:3] +
                   imdata.__next__()[:3] +
                   imdata.__next__()[:3]]
            
            for j in range(0, 8):
                if (datalist[i][j] == '0') and (pix[j] % 2 != 0):
                    pix[j] -= 1
                elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1
            
            if (i == lendata - 1):
                if (pix[-1] % 2 == 0):
                    pix[-1] -= 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1
            
            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self, newimg, data):
        w = newimg.size[0]
        (x, y) = (0, 0)
        
        for pixel in self.modPix(newimg.getdata(), data):
            newimg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

    def enc_fun(self, text_area, myimg, key_area):
        data = text_area.get("1.0", "end-1c")
        key = key_area.get("1.0", "end-1c")
        
        if len(data) == 0:
            messagebox.showinfo("Alert", "Please enter a message to hide")
            return
            
        if len(key) == 0:
            messagebox.showinfo("Alert", "Please enter an encryption key")
            return
            
        try:
            newimg = myimg.copy()
            newmsg = encryptMessage(data, key)
            self.encode_enc(newimg, newmsg)
            
            temp = os.path.splitext(os.path.basename(myimg.filename))[0]
            save_path = tkinter.filedialog.asksaveasfilename(
                initialfile=f"{temp}_encoded",
                filetypes=[('PNG files', '*.png')],
                defaultextension=".png"
            )
            
            if save_path:
                newimg.save(save_path)
                messagebox.showinfo(
                    "Success",
                    "Message encoded successfully!\nSaved as: " + os.path.basename(save_path)
                )
                self.home(text_area.master)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encode message: {str(e)}")

    def home(self, frame):
        frame.destroy()
        self.main(root)

if __name__ == "__main__":
    root = Tk()
    app = ModernStegno()
    app.main(root)
    root.mainloop()