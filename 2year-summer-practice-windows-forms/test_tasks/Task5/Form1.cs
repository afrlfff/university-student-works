using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Task5
{
    public partial class Form1 : Form
    {
        int[] m_p = new int[5];

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            this.Text = "Рисуем Линию";
            button1.Text = "Рисовать";
        }

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                m_p[1] = Convert.ToInt32(textBox1.Text);
                m_p[2] = Convert.ToInt32(textBox2.Text);
                m_p[3] = Convert.ToInt32(textBox3.Text);
                m_p[4] = Convert.ToInt32(textBox4.Text);
                pictureBox1.Refresh();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Некорректно заданы координаты.", "Ошибка");
            }
        }

        private void pictureBox1_Paint(object sender, PaintEventArgs e)
        {
            e.Graphics.DrawLine(System.Drawing.Pens.Green, m_p[1], m_p[2], m_p[3], m_p[4]);
        }
    }
}
