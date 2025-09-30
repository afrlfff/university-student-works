using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Task3
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            this.Text = "Фото галерея";
            label1.Text = "";
            comboBox1.Text = "Список";
        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            switch (comboBox1.SelectedIndex) {
                case 0:
                    pictureBox1.Image = Image.FromFile("C:\\Users\\DNS\\Documents\\Alexander_Frolov\\программы ЛЭТИ\\2_year\\Учебная_практика_C++\\Ознакомительные задания\\Task3\\img\\кот.jpg");
                    label1.Text = "Кот";
                    break;
                case 1:
                    pictureBox1.Image = Image.FromFile("C:\\Users\\DNS\\Documents\\Alexander_Frolov\\программы ЛЭТИ\\2_year\\Учебная_практика_C++\\Ознакомительные задания\\Task3\\img\\собака.jpg");
                    label1.Text = "Собака";
                    break;
                case 2:
                    pictureBox1.Image = Image.FromFile("C:\\Users\\DNS\\Documents\\Alexander_Frolov\\программы ЛЭТИ\\2_year\\Учебная_практика_C++\\Ознакомительные задания\\Task3\\img\\лес.jpg");
                    label1.Text = "Лес";
                    break;
                case 3:
                    pictureBox1.Image = Image.FromFile("C:\\Users\\DNS\\Documents\\Alexander_Frolov\\программы ЛЭТИ\\2_year\\Учебная_практика_C++\\Ознакомительные задания\\Task3\\img\\смартфон.jpg");
                    label1.Text = "Смартфон";
                    break;
                default:
                    break;
            }
        }
    }
}
