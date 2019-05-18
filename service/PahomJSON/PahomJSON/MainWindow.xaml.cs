using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Microsoft.Win32;
using System.IO;
using System.Text.RegularExpressions;
using System.Media;

namespace PahomJSON
{
    /// <summary>
    /// Логика взаимодействия для MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private string fileContent = string.Empty;
        private string filePath = string.Empty;
        private string originalFile = string.Empty;
        private string writePath = "json\\";
        private StreamReader sr;
        private string[] jsons;
        private int page = 1;
        private string title = "";
        public MainWindow()
        {
            InitializeComponent();
            jsons = new string[31] { "kolsk","busy", "kit","bye", "army", "bio", "chasha","cinema", "culture", "emotion.agressive", "emotion.crazy", "emotion.negative", "emotion.positive", "facts", "god", "gta", "hello", "it", "minecraft", "navalny", "novel", "patriot", "photo", "politic", "pony", "putin", "ussr", "vacancy", "whoami", "work", "xj9" };
            next.Content = "Загрузи какой-нибудь файл";
        }
        int[] myIntArray = new int[5] { 1, 2, 3, 4, 5 };
        private void Button_Click(object sender, RoutedEventArgs e)
        {
            if (sound.IsChecked == true)
            {
                SoundPlayer simpleSound = new SoundPlayer("sound.wav");
                simpleSound.Play();
            }
            Button pressed = (Button)sender;
            addToFile(pressed.Tag.ToString(), txt.Text);
            
        }

        private void Button_Click_1(object sender, RoutedEventArgs e)
        {
            next.Content = "Далее";
            int neededPage = int.Parse(pages.Text);
            if (neededPage == 0)
            {
                page++;

                this.Title = page.ToString() + "строка " + title;

                txt.Text = sr.ReadLine();
                
            }
            else
            {
                sr = new StreamReader(originalFile, Encoding.UTF8);
                page = 1;

                for (int i = page; i < neededPage; i++)

                {
                    page++;
                    this.Title = page.ToString() + " строка " + title;
                    txt.Text = sr.ReadLine();
                }
                pages.Text = "0";

            }
            string pattern = @"(\[id(.*?)\])";
            string pattern2 = @"(\[club(.*?)\])";
            string pattern3 = "(\",)";
            string pattern4 = "(\")";
            txt.Text = Regex.Replace(txt.Text, pattern, "ANONIM");
            txt.Text = Regex.Replace(txt.Text, pattern2, "ANONIM");
            txt.Text = Regex.Replace(txt.Text, pattern3, "");
            txt.Text = Regex.Replace(txt.Text, pattern4, "");

            next.Content = "Далее";

        }

        private void Button_Click_2(object sender, RoutedEventArgs e)
        {

        }

        private void Button_Click_3(object sender, RoutedEventArgs e)
        {

        }

        private void Button_Click_4(object sender, RoutedEventArgs e)
        {
            OpenFileDialog window = new OpenFileDialog();
            
            window.DefaultExt = ".txt";
            window.Filter = "Бредни пахома (.txt)|*.txt";

            Nullable<bool> result = window.ShowDialog();

            if (result == true)
            {
                next.Content = "Далее";
                originalFile = window.FileName;
                this.Title = "PahomJSON" + " Файл: " + originalFile;
                title = "PahomJSON" + " Файл: " + originalFile;
                this.Title = page.ToString() + "строка " + title;
                sr = new StreamReader(originalFile, Encoding.UTF8);
                page = 0;
                pages.Text = page.ToString();
                //sr = new StreamReader(originalFile, Encoding.GetEncoding(1251));
                
                sr = File.OpenText(originalFile);
                txt.Text = sr.ReadLine();
                
            }
        }
        private void addToFile(string file, string content)
        {
            using (StreamWriter sw = new StreamWriter(writePath + "pahom.agent." +file + ".json", true, System.Text.Encoding.UTF8))
            {
                sw.WriteLine("\"" +content + "\",");
            }
        }
        private void Button_Click_5(object sender, RoutedEventArgs e)
        {
            string message = "Будут сгенерированы заголовки для всех несуществующих тем. Те файлы, что уже сформированы, не будут затронуты. Актуально, если были добавлены дополнительные кнопки в форме + добавлен ее тег в массив json.";
            string caption = "Шухер нах! Алерт нах!";
            MessageBoxButton buttons = MessageBoxButton.YesNo;
            MessageBoxResult result;

            result = MessageBox.Show(message, caption, buttons,
            MessageBoxImage.Question);

            if (result == MessageBoxResult.Yes)
            {
                for (int i = 0; i < jsons.Length; i++)
                {
                   string path = writePath + "pahom.agent." + jsons[i] + ".json";

                   if ( File.Exists(path) == false)
                    {
                        using(StreamWriter sw = new StreamWriter(path, true, System.Text.Encoding.UTF8))
                    {
                            sw.WriteLine("{");
                            sw.WriteLine("\"id\": \"\",");
                            sw.WriteLine("\"name\": \"pahom.agent." + jsons[i] + "\",");
                            sw.WriteLine("\"auto\": true,");
                            sw.WriteLine("\"contexts\": [],");
                            sw.WriteLine("\"responses\": [");
                            sw.WriteLine("    {");
                            sw.WriteLine("\"resetContexts\": false,");
                            sw.WriteLine("\"affectedContexts\": [],");
                            sw.WriteLine("\"parameters\": [],");
                            sw.WriteLine("\"messages\": [");
                            sw.WriteLine("    {");
                            sw.WriteLine("          \"type\": 0,");
                            sw.WriteLine("          \"lang\": \"ru\",");
                            sw.WriteLine("          \"speech\": [");

                        }
                    }

                 
                }
            }
            
        }

        private void Button_Click_6(object sender, RoutedEventArgs e)
        {

        }

        private void Button_Click_7(object sender, RoutedEventArgs e)
        {
            OpenFileDialog window = new OpenFileDialog();

            window.DefaultExt = ".json";
            window.Filter = "Отсортированные бредни пахома (.json)|*.json";

            Nullable<bool> result = window.ShowDialog();

            if (result == true)
            {
                FileInfo fileInfo = new FileInfo(window.FileName);
                writePath = fileInfo.DirectoryName + "\\";
                MessageBox.Show(writePath);
                
            }
        }

        private void Button_Click_8(object sender, RoutedEventArgs e)
        {
            string message = "При нажатии на кнопку ОК, удалится с последней записи в массиве запятая и после запишется остаточная часть жсон файлов, крч нажимать если уже весь бред пахома распределили и пора отправлять эти жсоны в гугл. ";
            string caption = "Шухер нах! Алерт нах!";
            MessageBoxButton buttons = MessageBoxButton.YesNo;
            MessageBoxResult result;

            result = MessageBox.Show(message, caption, buttons,
            MessageBoxImage.Question);

            if (result == MessageBoxResult.Yes)
            {
                for (int i = 0; i < jsons.Length; i++)
                {
                    string path = writePath + "pahom.agent." + jsons[i] + ".json";
                    string[] text = File.ReadAllLines(path);
                    text[text.Length-1] = text[text.Length - 1].TrimEnd(text[text.Length - 1][text[text.Length - 1].Length - 1]);
                    File.WriteAllLines(path, text);

                    using (StreamWriter sw = new StreamWriter(path, true, System.Text.Encoding.UTF8))
                    {
                        sw.WriteLine("          ]");
                        sw.WriteLine("        }");
                        sw.WriteLine("      ],");
                        sw.WriteLine("      \"defaultResponsePlatforms\": {},");
                        sw.WriteLine("      \"speech\": []");
                        sw.WriteLine("    }");
                        sw.WriteLine("  ],");
                        sw.WriteLine("  \"priority\": 500000,");
                        sw.WriteLine("  \"webhookUsed\": false,");
                        sw.WriteLine("  \"webhookForSlotFilling\": false,");
                        sw.WriteLine("  \"fallbackIntent\": false,");
                        sw.WriteLine("  \"events\": []");
                        sw.WriteLine("}");
                    }
                }

            }

        }

        private void Pages_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (pages.Text != "0" || pages.Text != String.Empty)
            {
                next.Content = "Перейти";
            }
            else
            {
                next.Content = "Далее";
            }
        }

        private void Button_Click_9(object sender, RoutedEventArgs e)
        {
            string message = "Будут удалены подвалы со всех файлов. Перед отправкой в гугл не забудь опять сгенерить подвалы)00 и добавлена злоебучая запятая в конец.";
            string caption = "Шухер нах! Алерт нах!";
            MessageBoxButton buttons = MessageBoxButton.YesNo;
            MessageBoxResult result;

            result = MessageBox.Show(message, caption, buttons,
            MessageBoxImage.Question);

            if (result == MessageBoxResult.Yes)
            {
                for (int i = 0; i < jsons.Length; i++)
                {
                    string path = writePath + "pahom.agent." + jsons[i] + ".json";
                    File.WriteAllLines(path, File.ReadAllLines(path).Reverse().Skip(13).Reverse());
                    string[] text = File.ReadAllLines(path);
                    text[text.Length - 1] = text[text.Length - 1] + ",";
                    File.WriteAllLines(path, text);

                }
            }
               
        }

        private void Button_Click_10(object sender, RoutedEventArgs e)
        {
            string message = "Файлы usersays будут сгенерированы в папке json_usersays в целевой папке";
            string caption = "Шухер нах! Алерт нах!";
            MessageBoxButton buttons = MessageBoxButton.YesNo;
            MessageBoxResult result;

            result = MessageBox.Show(message, caption, buttons,
            MessageBoxImage.Question);

            if (result == MessageBoxResult.Yes)
            {
               
                for (int i = 0; i < jsons.Length; i++)
                {
                    string path = writePath + "json_usersays\\" + "pahom.agent." + jsons[i] + "_usersays_ru.json";

                    if (File.Exists(path) == false)
                    {
                        using (StreamWriter sw = new StreamWriter(path, true, System.Text.Encoding.UTF8))
                        {
                            sw.WriteLine("[");
                            sw.WriteLine("{");
                            sw.WriteLine("    \"id\": \"\",");
                            sw.WriteLine("    \"data\": [");
                            sw.WriteLine("      {");
                            sw.WriteLine("        \"text\": \"\",");
                            sw.WriteLine("        \"userDefined\": false");
                            sw.WriteLine("      }");
                            sw.WriteLine("    ],");
                            sw.WriteLine("    \"isTemplate\": false,");
                            sw.WriteLine("    \"count\": 0");
                            sw.WriteLine("    }");
                            sw.WriteLine("]");
                        }
                    }


                }

            }
        }
    }
}
