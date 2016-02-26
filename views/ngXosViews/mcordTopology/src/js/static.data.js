'use strict';

angular.module('xos.mcordTopology')
.constant('TopologyElements', {
  nodes: [
    {
      id: 'fabric1',
      type: 'fabric',
      name: 'fabric1',
      fixed: true,
      x: 1,
      y: 1
    },
    {
      id: 'fabric2',
      type: 'fabric',
      name: 'fabric2',
      fixed: true,
      x: 1,
      y: 2
    },
    {
      id: 'fabric3',
      type: 'fabric',
      name: 'fabric3',
      fixed: true,
      x: 2,
      y: 1
    },
    {
      id: 'fabric4',
      type: 'fabric',
      name: 'fabric4',
      fixed: true,
      x: 2,
      y: 2
    }
  ],
  links: [
    {
      source: 'fabric1',
      target: 'fabric2'
    },
    {
      source: 'fabric1',
      target: 'fabric4'
    },
    {
      source: 'fabric3',
      target: 'fabric4'
    },
    {
      source: 'fabric3',
      target: 'fabric2'
    }
  ],
  icons: {
    bbu: `M15,100a5,5,0,0,1-5-5v-65a5,5,0,0,1,5-5h80a5,5,0,0,1,5,5v65a5,5,0,0,1-5,5zM14,22.5l11-11a10,3,0,0,1,10-2h40a10,3,0,0,1,10,2l11,11zM16,35a5,5,0,0,1,10,0a5,5,0,0,1-10,0z`,
    switch: `M10,20a10,10,0,0,1,10-10h70a10,10,0,0,1,10,10v70a10,10,
            0,0,1-10,10h-70a10,10,0,0,1-10-10zM60,26l12,0,0-8,18,13-18,13,0
            -8-12,0zM60,60l12,0,0-8,18,13-18,13,0-8-12,0zM50,40l-12,0,0-8
            -18,13,18,13,0-8,12,0zM50,74l-12,0,0-8-18,13,18,13,0-8,12,0z`,
    rru: `M85,71.2c-8.9,10.5-29.6,8.7-45.3-3.5C23.9,55.4,19.8,37,28.6,26.5C29.9,38.6,71.5,69.9,85,71.2z M92.7,76.2M16.2,15 M69.5,100.7v-4c0-1.4-1.2-2.2-2.6-2.2H19.3c-1.4,0-2.8,0.7-2.8,2.2v3.9c0,0.7,0.8,1,1.5,1h50.3C69,101.5,69.5,101.3,69.5,100.7z M77.3,7.5l0,3.7c9,0.1,16.3,7.1,16.2,15.7l3.9,0C97.5,16.3,88.5,7.6,77.3,7.5z M77.6,14.7l0,2.5c5.3,0,9.7,4.2,9.6,9.3l2.6,0C89.9,20,84.4,14.7,77.6,14.7z M82.3,22.2c-1.3-1.2-2.9-1.9-4.7-1.9l0,1.2c1.4,0,2.8,0.6,3.8,1.5c1,1,1.6,2.3,1.6,3.7l1.3,0C84.3,25.1,83.6,23.4,82.3,22.2z M38.9,69.5l-5.1,23h16.5l-2.5-17.2C44.1,73.3,38.9,69.5,38.9,69.5zM58.1,54.1c13.7,10.1,26.5,16.8,29.2,13.7c2.7-3.1-5.6-13-19.3-24.4 M62.9,34.2 M62,37.9C47.7,27.3,33.7,20,31,23.1c-2.7,3.2,7,14.2,20.6,26 M73.9,25.7c-2.9,0.1-5.2,2.3-5.1,4.8c0,0.7,0.2,1.4,0.6,2l0,0L53.8,49.7l3.3,2.5L72.7,35l-0.4-0.3c0.6,0.2,1.3,0.3,1.9,0.3c2.9-0.1,5.2-2.3,5.1-4.9C79.3,27.6,76.8,25.6,73.9,25.7z`
  }
})