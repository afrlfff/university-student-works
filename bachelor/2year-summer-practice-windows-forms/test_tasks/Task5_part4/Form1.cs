using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Reflection.Emit;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;

namespace Task5
{
    public partial class Form1 : Form
    {
        int[] m_p = new int[7];
        int index;

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            this.Text = "Закрашивание фигур";
            label1.Text = "Выберите фигуру";
            comboBox1.Text = "Фигуры";
            pictureBox1.BackColor = Color.White;
            ArrayList Фигуры = new ArrayList { "Прямоугольник", "Эллипс", "Окружность" };
            comboBox1.Items.AddRange(Фигуры.ToArray());
        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            Graphics Графика = pictureBox1.CreateGraphics();
            Brush Заливка = new SolidBrush(Color.Orange);
            Графика.Clear(Color.White);
            switch (comboBox1.SelectedIndex)
            {
                case 0:
                    Графика.FillRectangle(Заливка, 60, 60, 120, 180); break;
                case 1:
                    Графика.FillEllipse(Заливка, 60, 60, 120, 180); break;
                case 2:
                    Графика.FillEllipse(Заливка, 60, 60, 120, 120); break;

            }
        }
    }
}
