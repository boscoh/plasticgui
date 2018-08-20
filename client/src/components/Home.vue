<template>
  <v-container
      fluid
      grid-list-xl>

    <v-layout
        row
        wrap>
      <v-flex xs12>
        <h2>
          Example Widgets
        </h2>
      </v-flex>
    </v-layout>

    <v-layout
        row
        wrap>

      <v-flex xs4>
        <v-card height="100%">
          <v-card-title
              primary-title
              class="headline">
            Webgl 3D Graphics
          </v-card-title>
          <v-card-text>
            <div
                style="width: 100%; height: 200px"
                id="webgl">
            </div>
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex xs4>
        <v-card height="100%">
          <v-card-title
              primary-title
              class="headline">
            Canvas 2d Graphics
          </v-card-title>
          <v-card-text>
            <div
                id="rect"
                style="width: 200px; height: 200px">
            </div>
            {{ pointerX }} - {{ pointerY }}
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex xs4>
        <v-card height="100%">
          <v-card-title
            primary-title
            class="headline">
            Live graphs
          </v-card-title>
          <v-card-text>
            <div id="sliders">
              <v-layout
                row
                v-for="(param, i) of sliders"
                :key="i">
                <v-flex xs4>
                  {{param.key}} = {{param.value.toFixed(1)}}
                </v-flex>
                <v-flex xs8>
                  <v-slider
                    ref="slider"
                    :step="param.interval"
                    @callback="changeGraph()"
                    :max="param.max"
                    v-model="param.value" />
                </v-flex>
              </v-layout>
            </div>
            <div style="margin-top: 1em">
              <v-btn @click="randomizeGraph()">
                random
              </v-btn>
            </div>
            <v-layout>
              <v-flex
                xs12
                id="charts">
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-flex>

    </v-layout>

    <v-layout
        row
        wrap>

      <v-flex xs4>
        <v-card height="100%">
          <v-card-title
            primary-title
            class="headline">
            Server text
          </v-card-title>
          <v-card-text>
            {{ text }}
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex xs4>
        <v-card height="100%">
          <v-card-title
            primary-title
            class="headline">
            File Download
          </v-card-title>
          <v-card-text>
            <div>
              <v-btn @click="getReadme()">
                Download Readme.md
              </v-btn>
            </div>
            <div>
              <v-btn @click="getLogoPng()">
                Download Logo.png
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex xs4>
        <v-card height="100%">
          <v-card-title
            primary-title
            class="headline">
            File Upload
          </v-card-title>
          <v-card-text>
            <upload-button
              title="Upload"
              :selectedCallback="fileSelectedFunc"/>
            <v-list>
              <v-list-tile v-for="file, i in uploadFiles" :key="i">
                <a :href="file.url">{{file.name}}</a>
              </v-list-tile>
            </v-list>
          </v-card-text>
        </v-card>
      </v-flex>


    </v-layout>
  </v-container>
</template>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped>
#sliders div {
  margin: 0px;
  padding: 0px;
}
</style>

<script>
import _ from 'lodash'

import rpc from '../modules/rpc'
import vueSlider from 'vue-slider-component'
import config from '../config'
import ChartWidget from '../modules/chart-widget'
import CanvasWidget from '../modules/canvas-widget'
import Model from '../modules/model'
import webglstarterkit from '../modules/webgl-widget'
import UploadButton from './UploadButton'

const THREE = require('three')

function getRandomColor () {
  let letters = '0123456789ABCDEF'
  let color = '#'
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)]
  }
  return color
}

export default {
  name: 'experiments',
  components: {vueSlider, UploadButton},
  data () {
    return {
      text: '',
      error: '',
      pointerX: 0,
      pointerY: 0,
      uploadFiles: [],
      sliders: [
        {
          key: 'alpha',
          value: 1,
          max: 10,
          interval: 0.1
        },
        {
          key: 'beta',
          value: 1,
          max: 7,
          interval: 0.1
        },
        {
          key: 'gamma',
          value: 0.5,
          max: 10,
          interval: 0.1
        }
      ]
    }
  },
  async mounted () {
    let params = {}
    for (let slider of this.sliders) {
      params[slider.key] = slider.value
    }

    this.model = new Model(params)
    this.model.initializeVars = function () {
      this.vars.y = 0
    }
    this.model.update = function (iStep) {
      this.vars.y =
        this.params.alpha *
        Math.sin(this.params.beta * iStep + this.params.gamma)
    }

    this.chartWidget = new ChartWidget('#charts')
    this.chartWidget.setTitle('title')
    this.chartWidget.setXLabel('xLabel')
    this.chartWidget.setYLabel('yLabel')
    this.chartWidget.addDataset('sample')
    this.randomizeGraph()

    this.canvasWidget = new CanvasWidget('#rect')
    this.canvasWidget.drawWidth = this.canvasWidget.width()
    this.canvasWidget.drawHeight = this.canvasWidget.height()
    this.canvasWidget.mousemove = e => {
      this.canvasWidget.getPointer(event)
      this.canvasWidget.drawWidth = this.canvasWidget.pointerX
      this.canvasWidget.drawHeight = this.canvasWidget.pointerY
      this.pointerX = this.canvasWidget.pointerX.toFixed(0)
      this.pointerY = this.canvasWidget.pointerY.toFixed(0)
      this.drawCanvas()
    }
    this.drawCanvas()

    this.webglWidget = new webglstarterkit.WebglWidget('#webgl', '#FFFFFF')
    let geometry = new THREE.BoxGeometry(50, 32, 32)
    let material = new THREE.MeshPhongMaterial({
      color: 0x156289,
      emissive: 0x072534,
      side: THREE.DoubleSide,
      flatShading: true
    })
    this.webglWidget.scene.add(new THREE.Mesh(geometry, material))
    this.webglWidget.moveCameraToShowAll()
    this.webglWidget.update = () => {
      this.webglWidget.rotateCameraAroundScene(0.005, 0.01, 0)
    }
    this.webglWidget.draw()

    let response = await rpc.rpcRun('publicGetText')
    if (response.result) {
      this.text = response.result.text
    } else {
      this.error = response.error.message
    }
  },
  watch: {
    sliders: {
      handler () {
        this.changeGraph()
      },
      deep: true
    }
  },
  methods: {
    async getReadme () {
      let response = await rpc.rpcDownload('publicDownloadGetReadme')
      if (response.error) {
        this.error = response.error.message
      }
    },
    async getLogoPng () {
      let response = await rpc.rpcDownload('publicDownloadLogo')
      if (response.error) {
        this.error = response.error.message
      }
    },
    drawCanvas () {
      for (let i = 0; i < 10; i += 1) {
        let x1 = Math.random() * this.canvasWidget.drawWidth
        let y1 = Math.random() * this.canvasWidget.drawHeight
        let x2 = Math.random() * (this.canvasWidget.drawWidth - x1)
        let y2 = Math.random() * (this.canvasWidget.drawHeight - y1)
        this.canvasWidget.fillRect(x1, y1, (x2 - x1), (y2 - y1), getRandomColor())
      }
    },
    selectFiles (filelist) {
      this.filelist = filelist
    },
    async upload () {
      this.uploadFiles = []
      if (this.filelist) {
        this.error = ''
        let response = await rpc.rpcUpload('publicUploadFiles', this.filelist)
        if (response.result) {
          this.uploadFiles = _.map(response.result.files, f => config.apiUrl + f)
        } else {
          this.error = response.error.message
        }
      } else {
        this.error = 'No files selected'
      }
    },
    changeGraph () {
      console.log('changed graph', this.sliders)
      for (let slider of this.sliders) {
        this.model.params[slider.key] = slider.value
      }
      let nStep = 100
      let xValues = _.range(0, nStep)
      this.model.resetSoln()
      this.model.integrate(nStep)
      let yValues = this.model.soln.y
      this.chartWidget.updateDataset(0, xValues, yValues)
    },
    randomizeGraph () {
      for (let slider of this.sliders) {
        slider.value = Math.random() * slider.max
      }
      this.changeGraph()
    },
    async fileSelectedFunc (files) {
      let response = await rpc.rpcUpload('publicUploadFiles', files)
      this.uploadFiles.length = 0
      for (let f of response.result.files) {
        this.uploadFiles.push({ name: f, url: 'http://localhost:3000' + f})
      }
    }
  }
}
</script>
