using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace DongThamChieu
{
    
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        private HttpClient client = new HttpClient();

        string chuoiJSON = "";
        string caucuoi = "";
        string capthaythe = "";
        List<string> ketquadongthamchieu = new List<string>();
        List<string> danhsachthucthe = new List<string>();
        private void btnDatLai_Click(object sender, EventArgs e)
        {
            rtbShow.Clear();
            lbTitle.Text = "Bài toán đồng tham chiếu";
            txtCau.Clear();
            btnALL.Enabled = false;
            btnListThucThe.Enabled = false;
            btnListThayThe.Enabled = false;
            btnKQDTC.Enabled = false;
            btnDatLai.Enabled = false;
        }

        private void btnListThucThe_Click(object sender, EventArgs e)
        {
            rtbShow.Clear();
            lbTitle.Text = "Danh sách các thực thể";
            if (danhsachthucthe != null && danhsachthucthe.Count > 0)
            {
                foreach (string item in danhsachthucthe)
                {
                    rtbShow.AppendText(item + Environment.NewLine);
                }
            }
            else
            {
                rtbShow.Text = "danhsachthucthe chưa có giá trị hoặc là một danh sách rỗng.";
            }
        }

        private void btnThoat_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private async void btnThucHien_ClickAsync(object sender, EventArgs e)
        {
            string cau = txtCau.Text;
            if(String.IsNullOrWhiteSpace(cau))
            {
                MessageBox.Show("Nội dung không hợp lệ", "Lỗi");
            }
            else
            {
                pbLoad.Visible = true;
                trangthai(false);
                try
                {
                    chuoiJSON = await SendRequestAsync(cau);
                    ProcessJsonData(chuoiJSON);

                    rtbShow.Text = chuoiJSON;
                }
                catch (Exception ex)
                {
                    rtbShow.Text = "Có lỗi xảy ra khi gửi yêu cầu: " + ex.Message;
                }
                finally
                {
                    pbLoad.Visible = false;
                    trangthai(true);
                }
            }
        }

        private async Task<string> SendRequestAsync(string input)
        {
            string apiUrl = "http://127.0.0.1:8000/dong-tham-chieu/";

            var requestData = new
            {
                cau = input
            };

            var json = JsonConvert.SerializeObject(requestData);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            HttpResponseMessage response = await client.PostAsync(apiUrl, content);
            if (response.IsSuccessStatusCode)
            {
                string responseContent = await response.Content.ReadAsStringAsync();
                string apiResponse = JsonConvert.DeserializeObject<string>(responseContent);
                return apiResponse;
            }
            else
            {
                throw new Exception("Lỗi HTTP: " + response.StatusCode);
            }
        }
        public void ProcessJsonData(string jsonData)
        {
            JObject jsonObject = JObject.Parse(jsonData);

            caucuoi = (string)jsonObject["caucuoi"];
            capthaythe = jsonObject["capthaythe"].ToObject<string>();
            ketquadongthamchieu = jsonObject["ketquadongthamchieu"].ToObject<List<string>>();
            danhsachthucthe = jsonObject["danhsachthucthe"].ToObject<List<string>>();

            //rtbShow.Text = caucuoi;
        }
        private void trangthai(Boolean t)
        {
            txtCau.Enabled = t;
            btnALL.Enabled = t;
            btnKQDTC.Enabled = t;
            btnListThucThe.Enabled = t;
            btnListThayThe.Enabled = t;
            btnThoat.Enabled = t;
            btnThucHien.Enabled = t;
            btnDatLai.Enabled = t;
            btnTongQuan.Enabled = t;
        }

        private void btnALL_Click(object sender, EventArgs e)
        {
            rtbShow.Clear();
            lbTitle.Text = "Câu đã thay thế";
            if (!String.IsNullOrEmpty(caucuoi))
            {
                rtbShow.Text = caucuoi;
            }
            else
            {
                rtbShow.Text = "Chưa có giá trị";
            }
        }

        private void btnListThayThe_Click(object sender, EventArgs e)
        {
            rtbShow.Clear();
            lbTitle.Text = "Danh sách thay thế thực thể";
            if (!string.IsNullOrEmpty(capthaythe))
            {
                rtbShow.Text = capthaythe;
            }
            else
            {
                rtbShow.Text = "capthaythe chưa có giá trị.";
            }
        }

        private void btnKQDTC_Click(object sender, EventArgs e)
        {
            rtbShow.Clear();
            lbTitle.Text = "Kết quả tham chiếu các cặp thực thể";
            if (ketquadongthamchieu != null && ketquadongthamchieu.Count > 0)
            {
                foreach (string item in ketquadongthamchieu)
                {
                    rtbShow.AppendText(item + Environment.NewLine);
                }
            }
            else
            {
                rtbShow.Text = "ketquadongthamchieu chưa có giá trị hoặc là một danh sách rỗng.";
            }
        }

        private void btnTongQuan_Click(object sender, EventArgs e)
        {
            lbTitle.Text = "Bài toán đồng tham chiếu";
            rtbShow.Clear();
            rtbShow.AppendText(txtCau.Text + Environment.NewLine);
            rtbShow.AppendText("=================== Thực Thể ===================" + Environment.NewLine);
            if (danhsachthucthe != null && danhsachthucthe.Count > 0)
            {
                foreach (string item in danhsachthucthe)
                {
                    rtbShow.AppendText(item + Environment.NewLine);
                }
            }
            rtbShow.AppendText("=================== Kết quả tham chiếu ===================" + Environment.NewLine);
            if (ketquadongthamchieu != null && ketquadongthamchieu.Count > 0)
            {
                foreach (string item in ketquadongthamchieu)
                {
                    rtbShow.AppendText(item + Environment.NewLine);
                }
            }
            rtbShow.AppendText("=================== Danh sách thay thế thực thể ===================" + Environment.NewLine);
            if (!string.IsNullOrEmpty(capthaythe))
            {
                rtbShow.AppendText(capthaythe + Environment.NewLine);
            }
            rtbShow.AppendText("=================== Câu đã thay thế ===================" + Environment.NewLine);
            if (!String.IsNullOrEmpty(caucuoi))
            {
                rtbShow.AppendText(caucuoi + Environment.NewLine);
            }
        }
    }
}
