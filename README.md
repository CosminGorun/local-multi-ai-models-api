<h2 align="center">Local Multi AI Models API</h2>

<hr>

<h3>How to Run</h3>
<p>
Run the <code>runner.py</code> script.<br>
This will execute the command:<br>
<code>uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)</code><br>
and start a server on port <strong>8000</strong>.
</p>

<p>
The API uses <strong>FastAPI</strong>. This project is a work in progress.
</p>

<hr>

<h3>Available Classes</h3>

<h4>1) custom_model</h4>
<p>
This class imports and uses a pre-installed model from <strong>Hugging Face</strong>.<br>
It provides the following endpoints:
</p>

<ul>
<li><strong>POST</strong>:
  <ul>
    <li><code>/initModel</code> – loads the model into memory.</li>
    <li><code>/delModel</code> – frees the model from memory.</li>
  </ul>
</li>
<li><strong>GET</strong>:
  <ul>
    <li><code>/getResponse</code> – returns a string with the model's response.</li>
  </ul>
</li>
</ul>

<h4>2) generator3D</h4>
<p>
Generates a 3D object from text or image using <strong>Shap-E</strong>.
</p>

<h4>3) openrouter_deepseek</h4>
<p>
Calls the <strong>DeepSeek</strong> free model using <strong>OpenRouter</strong>.
</p>

<hr>

<h3>Status</h3>
<p>
This project is under active development. The code may change, so this README might refer to an older version.<br>
All dependencies are listed in the <code>requirements.txt</code> file.
</p>
