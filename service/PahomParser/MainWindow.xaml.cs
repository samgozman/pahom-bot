namespace PahomVKParser
{
    using System.IO;
    using System.Threading.Tasks;
    using System.Windows;
    using VkNet;
    using VkNet.Enums.Filters;
    using VkNet.Model;
    using VkNet.Model.RequestParams;

    /// <summary>
    /// Логика взаимодействия для MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        /// <summary>
        /// Путь для записи постов в файл.
        /// </summary>
        internal string writePath = @"C:\Users\wapif\Documents\pahom.txt";

        /// <summary>
        /// Путь для записи идентификаторов постов, которых не удалось спарсить.
        /// </summary>
        internal string writeError = @"C:\Users\wapif\Documents\error.txt";

        /// <summary>
        /// Defines the vk
        /// </summary>
        public VkApi vk = new VkApi();

        /// <summary>
        /// Initializes a new instance of the <see cref="MainWindow"/> class.
        /// </summary>
        public MainWindow()
        {
            InitializeComponent();
            AddToLog("Инициализация");
            res.AcceptsReturn = true;
            AddToRes("{");
            AddToRes("goodThink:[");
        }

        /// <summary>
        /// Функция добавления в текстбокс логов
        /// </summary>
        /// <param name="txt">Строка, загружаемая в лог<see cref="string"/></param>
        private void AddToLog(string txt)
        {
            log.AppendText(txt + "\n");
            log.SelectionStart = log.Text.Length;
            log.ScrollToEnd();
        }

        /// <summary>
        /// Функция для добавления в текстбокс и построчной записи найденых постов пахома
        /// </summary>
        /// <param name="txt">Строка, записываемая в файл.<see cref="string"/></param>
        private void AddToRes(string txt)
        {
            res.AppendText(txt + "\n");
            res.SelectionStart = res.Text.Length;
            res.ScrollToEnd();
            using (StreamWriter sw = new StreamWriter(writePath, true, System.Text.Encoding.Default))
            {
                sw.WriteLine(txt);
            }
        }

        /// <summary>
        /// Функция добавления идентификаторов неудачных парсов
        /// </summary>
        /// <param name="txt">Идентификатор поста<see cref="string"/></param>
        private void AddToError(string txt)
        {
            AddToLog("ОШИБКА! ПОСТ " + txt);
            using (StreamWriter sw = new StreamWriter(writeError, true, System.Text.Encoding.Default))
            {
                sw.WriteLine(txt);
            }
        }

        /// <summary>
        /// Авторизация ВК апи по логину и паролю
        /// </summary>
        /// <param name="sender">The sender<see cref="object"/></param>
        /// <param name="e">The e<see cref="RoutedEventArgs"/></param>
        private void Button_Click(object sender, RoutedEventArgs e)
        {
            //Авторизация

            vk.Authorize(new ApiAuthParams
            {
                ApplicationId = 5648678,
                Login = login.Text,
                Password = password.Password,
                Settings = Settings.All
            }
            );

            AddToLog("Получен токен");
        }

        /// <summary>
        /// Получение постов. Метод vk api: wall.get
        /// </summary>
        /// <param name="sender">The sender<see cref="object"/></param>
        /// <param name="e">The e<see cref="RoutedEventArgs"/></param>
        private async void Button_Click_1(object sender, RoutedEventArgs e)
        {
            long? postid = 0;
            var wallGet = vk.Wall.Get(new WallGetParams
            {
                OwnerId = long.Parse(group_id.Text) * -1,
                Offset = 0,
                Count = 100
            }
            );
            int pahom = 0;
            progress.Maximum = wallGet.TotalCount;
            AddToLog("Всего записей " + wallGet.TotalCount.ToString());

            for (ulong k = 0; k < wallGet.TotalCount / 100 + 1; k++)
            {

                wallGet = vk.Wall.Get(new WallGetParams
                {
                    OwnerId = long.Parse(group_id.Text) * -1,
                    Offset = 100 * k,
                    Count = 100
                });
                for (int i = 0; i < wallGet.WallPosts.Count; i++)
                {
                    AddToLog("Поиск комментариев в посте №" + (100 * (int)k + i).ToString() + " из " + wallGet.TotalCount.ToString());
                    progress.Value = (100 * (int)k + i);
                    postid = wallGet.WallPosts[i].Id;
                    if (parsePosts.IsChecked == true && wallGet.WallPosts[i].Text != "")
                    {
                        pahom++;
                        string txt = wallGet.WallPosts[i].Text;
                        txt = txt.Replace(System.Environment.NewLine, " ");
                        AddToRes("\"" + txt + "\",");
                    }
                    try
                    {
                        if (wallGet.WallPosts[(int)i].Comments.Count > 0)
                        {
                            await Task.Delay(200);
                            var commentsFromPost = vk.Wall.GetComments(new WallGetCommentsParams
                            {
                                OwnerId = long.Parse(group_id.Text) * -1,
                                PostId = long.Parse(postid.ToString()),
                                Count = 100
                            });

                            AddToLog("В посте №" + i.ToString() + " найдено " + commentsFromPost.TotalCount + " комментариев");
                            for (ulong g = 0; g < commentsFromPost.TotalCount / 100 + 1; g++)
                            {

                                var commentsFromPostIn = vk.Wall.GetComments(new WallGetCommentsParams
                                {
                                    OwnerId = long.Parse(group_id.Text) * -1,
                                    PostId = long.Parse(wallGet.WallPosts[i].Id.ToString()),
                                    Offset = 100 * (long)g,
                                    Count = 100
                                });

                                for (int j = 0; j < commentsFromPostIn.Count; j++)
                                {
                                    if (commentsFromPostIn[j].FromId.ToString() == user_id.Text)
                                    {
                                        if (parseComments.IsChecked == true)
                                        {
                                            pahom++;
                                            AddToLog("Найден коммент пахома! Всего " + pahom.ToString() + " комментариев");
                                            AddToRes("\"" + commentsFromPostIn[j].Text + "\",");
                                        }

                                    }

                                }
                                await Task.Delay(200);
                            }
                        }
                        else
                        {
                            AddToLog("В посте №" + i.ToString() + "нет комментариев ");
                        }
                    }
                    catch
                    {
                        AddToError(postid.ToString());
                        i++;
                    }
                }
                await Task.Delay(200);
            }
            AddToRes("]");
            AddToRes("}");
        }


        /// <summary>
        /// Функция ручного добавления записей извне. Просто нужно скопировать текст в нижнюю область и нажать на кнопку.
        /// </summary>
        /// <param name="sender">The sender<see cref="object"/></param>
        /// <param name="e">The e<see cref="RoutedEventArgs"/></param>
        private void Button_Click_3(object sender, RoutedEventArgs e)
        {
            AddToRes("\"" + res.Text + "\",");
            res.Text = "";
        }
    }
}
