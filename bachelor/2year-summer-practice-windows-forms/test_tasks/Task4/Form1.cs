using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Task4
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            this.Text = "Текстовый редактор";
            openFileDialog1.FileName = "D:\\ВУЗ\\Text2.txt";
            openFileDialog1.Filter = "Текстовые файлы (*.txt)|*.txt|All files (*.*)|*.*";
            saveFileDialog1.Filter = "Текстовые файлы (*.txt)|*.txt|All files (*.*)|*.*";
        }

        private void открытьToolStripMenuItem_Click(object sender, EventArgs e)
        {
            openFileDialog1.ShowDialog();
            if (openFileDialog1.FileName == null) return;
            try
            {
                StreamReader MyReader = new System.IO.StreamReader(openFileDialog1.FileName,
                                        System.Text.Encoding.GetEncoding(1251));
                textBox1.Text = MyReader.ReadToEnd();
                MyReader.Close();
            }
            catch (System.IO.FileNotFoundException ex)
            {
                MessageBox.Show(ex.Message + "\nФайл не найден", "Ошибка",
                                MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Ошибка",
                                MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
            }
        }

        private void сохранитьКакToolStripMenuItem_Click(object sender, EventArgs e)
        {
            saveFileDialog1.FileName = openFileDialog1.FileName;
            if (saveFileDialog1.ShowDialog() == System.Windows.Forms.DialogResult.OK) Save();
        }

        void Save()
        {
            try
            {
                StreamWriter MyWriter = new System.IO.StreamWriter(
                                            saveFileDialog1.FileName, false,
                                            System.Text.Encoding.GetEncoding(1251));
                MyWriter.Write(textBox1.Text);
                MyWriter.Close();
                textBox1.Modified = false;
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Ошибка",
                                MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
            }
        }

        private void выходToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (textBox1.Modified == false) return;

            var MeBox = MessageBox.Show(
                                    "Текст был изменѐн. \nСохранить изменения?", "Простой редактор",
                                    MessageBoxButtons.YesNoCancel, MessageBoxIcon.Exclamation);
            if (MeBox == System.Windows.Forms.DialogResult.No) return;
            if (MeBox == System.Windows.Forms.DialogResult.Cancel) e.Cancel = true;
            if (MeBox == System.Windows.Forms.DialogResult.Yes)
            {
                if (saveFileDialog1.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    Save(); return;
                }
                else e.Cancel = true;
            }
        }
    }
}
